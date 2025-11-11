"""
Сервис генерации решений комиссии ГСИ
На основе анализа реальных документов ПРЕДЛОЖЕНИЕ и СНЯТИЕ
"""
from typing import Dict, List, Optional


class CommissionRecommendationService:
    """
    Генерация решений и обоснований для комиссии ГСИ
    на основе анализа реальных документов
    """

    def generate_recommendation(
        self,
        evaluation_scores: Dict,
        violations: List[Dict],
        overall_summary: Dict,
        sort_record: Dict
    ) -> Dict:
        """
        Генерация решения комиссии с обоснованием

        Args:
            evaluation_scores: Балльные оценки (yield, quality, resistance)
            violations: Список нарушений от AlertService
            overall_summary: Общая сводка по сорту
            sort_record: Информация о сорте

        Returns:
            {
                'decision': 'PROPOSE_TO_REGISTRY' | 'PROPOSE_TO_REMOVE' | 'CONTINUE_TRIALS',
                'confidence': 'high' | 'medium' | 'low',
                'justification_text': str,
                'key_facts': List[str],
                'regions_summary': {
                    'exceeding': int,
                    'below': int,
                    'neutral': int,
                    'total': int
                },
                'risk_factors': List[str]
            }
        """
        # Извлекаем ключевые данные
        yield_details = evaluation_scores.get('detailed_scores', {}).get('yield', {})
        yield_score = evaluation_scores.get('yield_score')
        quality_score = evaluation_scores.get('quality_score')
        resistance_score = evaluation_scores.get('resistance_score')

        regions_exceeding = yield_details.get('regions_exceeding', 0)
        regions_below = yield_details.get('regions_below', 0)
        regions_neutral = yield_details.get('regions_neutral', 0)
        regions_breakdown = yield_details.get('regions_breakdown', [])

        # Вычисляем средневзвешенное процентное отклонение по урожайности стандарта
        avg_deviation_percent = 0.0
        if regions_breakdown:
            total_weight = 0
            weighted_sum = 0
            for region in regions_breakdown:
                standard_yield = region.get('standard_average_yield', 0)
                deviation_percent = region.get('deviation_percent', 0)
                if standard_yield and standard_yield > 0:
                    weighted_sum += deviation_percent * standard_yield
                    total_weight += standard_yield
            avg_deviation_percent = weighted_sum / total_weight if total_weight > 0 else 0

        # Используем gsu_total из overall_summary (общее количество ГСУ для группы культуры)
        total_regions = overall_summary.get('gsu_total', len(regions_breakdown))

        years_tested = overall_summary.get('overall_min_years_tested', 0)
        coverage_percent = overall_summary.get('overall_coverage_percent', 0)

        sort_name = sort_record.get('name', 'Неизвестно')

        # Проверка критических нарушений
        critical_violations = [v for v in violations if v.get('severity') == 'critical']
        has_critical_violations = len(critical_violations) > 0

        # Определение решения
        decision = self._determine_decision(
            yield_score=yield_score,
            regions_exceeding=regions_exceeding,
            regions_below=regions_below,
            regions_neutral=regions_neutral,
            total_regions=total_regions,
            years_tested=years_tested,
            has_critical_violations=has_critical_violations,
            sort_name=sort_name,
            regions_breakdown=regions_breakdown
        )

        # Расчет уровня уверенности
        confidence = self._calculate_confidence(
            decision=decision,
            yield_score=yield_score,
            regions_exceeding=regions_exceeding,
            total_regions=total_regions,
            years_tested=years_tested,
            coverage_percent=coverage_percent,
            has_critical_violations=has_critical_violations
        )

        # Генерация текста обоснования
        justification_text = self._generate_justification_text(
            decision=decision,
            sort_name=sort_name,
            yield_details=yield_details,
            quality_score=quality_score,
            resistance_score=resistance_score,
            years_tested=years_tested,
            coverage_percent=coverage_percent,
            total_regions=total_regions,
            regions_breakdown=regions_breakdown,
            critical_violations=critical_violations
        )

        # Извлечение ключевых фактов
        key_facts = self._extract_key_facts(
            decision=decision,
            yield_details=yield_details,
            quality_score=quality_score,
            resistance_score=resistance_score,
            years_tested=years_tested,
            coverage_percent=coverage_percent,
            regions_exceeding=regions_exceeding,
            total_regions=total_regions,
            violations=violations
        )

        # Извлечение факторов риска
        risk_factors = self._extract_risk_factors(
            decision=decision,
            violations=violations,
            yield_score=yield_score,
            years_tested=years_tested,
            coverage_percent=coverage_percent
        )

        return {
            'decision': decision,
            'confidence': confidence,
            'justification_text': justification_text,
            'key_facts': key_facts,
            'regions_summary': {
                'exceeding': regions_exceeding,
                'below': regions_below,
                'neutral': regions_neutral,
                'total': total_regions,
                'avg_deviation_percent': round(avg_deviation_percent, 1)
            },
            'risk_factors': risk_factors
        }

    def _determine_decision(
        self,
        yield_score: Optional[float],
        regions_exceeding: int,
        regions_below: int,
        regions_neutral: int,
        total_regions: int,
        years_tested: int,
        has_critical_violations: bool,
        sort_name: str,
        regions_breakdown: List[Dict]
    ) -> str:
        """
        Определение категории решения (согласно методике)

        PROPOSE_TO_REGISTRY:
        1. Сорт используется как стандарт (тестируется сам с собой):
           - Все отклонения ≈ 0%
           - Сорт == Стандарт
        2. Значительное превышение (методика):
           - yield_score >= 5 (≥8% превышение)
           - regions_exceeding >= 50%
           - нет critical violations
        3. Стандартные критерии:
           - yield_score >= 4 (3-8% превышение)
           - regions_exceeding >= 50%
           - years_tested >= 3
           - нет critical violations

        PROPOSE_TO_REMOVE:
        - yield_score <= 2
        - ИЛИ regions_exceeding == 0 (уступает везде) И есть уступающие регионы
        - ИЛИ critical violations

        CONTINUE_TRIALS:
        - все остальное
        """
        if yield_score is None or total_regions == 0:
            return 'CONTINUE_TRIALS'

        # СПЕЦИАЛЬНЫЙ СЛУЧАЙ: Сорт испытывается сам с собой как стандарт
        # Проверяем, что все регионы имеют deviation ≈ 0 и сорт == стандарт
        if regions_breakdown and yield_score == 3:
            is_self_standard = True
            for region in regions_breakdown:
                deviation = abs(region.get('deviation_percent', 0))
                standard_name = region.get('standard_name', '')

                # Если отклонение > 1% или стандарт не совпадает с сортом
                if deviation > 1.0 or (standard_name and standard_name != sort_name):
                    is_self_standard = False
                    break

            if is_self_standard and years_tested >= 3:
                # Сорт уже используется как стандарт → рекомендуем к реестру
                return 'PROPOSE_TO_REGISTRY'

        # Критерии для СНЯТИЯ
        if has_critical_violations:
            return 'PROPOSE_TO_REMOVE'

        if yield_score <= 2.0:
            return 'PROPOSE_TO_REMOVE'

        # Уступает везде (но только если действительно уступает, а не просто на уровне стандарта)
        if regions_exceeding == 0 and regions_below > 0 and total_regions > 0:
            return 'PROPOSE_TO_REMOVE'

        # Критерии для РЕЕСТРА
        exceeding_percent = (regions_exceeding / total_regions * 100) if total_regions > 0 else 0

        # По методике: ≥8% превышение → допуск к реестру (приоритет над длительностью)
        if (yield_score >= 5.0 and exceeding_percent >= 50):
            # Значительное превышение (≥8%) в большинстве регионов
            return 'PROPOSE_TO_REGISTRY'

        # Стандартные критерии для реестра (требуют 3 года испытаний)
        if (yield_score >= 4.0 and
            exceeding_percent >= 50 and
            years_tested >= 3):
            return 'PROPOSE_TO_REGISTRY'

        # Все остальное - ПРОДОЛЖИТЬ ИСПЫТАНИЯ
        return 'CONTINUE_TRIALS'

    def _calculate_confidence(
        self,
        decision: str,
        yield_score: Optional[float],
        regions_exceeding: int,
        total_regions: int,
        years_tested: int,
        coverage_percent: float,
        has_critical_violations: bool
    ) -> str:
        """
        Расчет уровня уверенности в решении

        Returns:
            'high' | 'medium' | 'low'
        """
        if yield_score is None:
            return 'low'

        exceeding_percent = (regions_exceeding / total_regions * 100) if total_regions > 0 else 0

        # Высокая уверенность
        if decision == 'PROPOSE_TO_REGISTRY':
            # Специальный случай: сорт используется как стандарт (yield_score == 3 и regions_exceeding == 0)
            if yield_score == 3 and regions_exceeding == 0 and years_tested >= 3:
                return 'high'  # Высокая уверенность - сорт уже является стандартом
            elif (yield_score >= 4.5 and
                exceeding_percent >= 75 and
                years_tested >= 3 and
                coverage_percent >= 60):
                return 'high'
            elif yield_score >= 4.0 and exceeding_percent >= 60:
                return 'medium'
            else:
                return 'low'

        elif decision == 'PROPOSE_TO_REMOVE':
            if has_critical_violations or yield_score <= 1.5:
                return 'high'
            elif yield_score <= 2.0 or regions_exceeding == 0:
                return 'medium'
            else:
                return 'low'

        else:  # CONTINUE_TRIALS
            if years_tested < 2 or coverage_percent < 30:
                return 'high'  # Уверенно нужны дополнительные данные
            else:
                return 'medium'

    def _generate_justification_text(
        self,
        decision: str,
        sort_name: str,
        yield_details: Dict,
        quality_score: Optional[float],
        resistance_score: Optional[float],
        years_tested: int,
        coverage_percent: float,
        total_regions: int,
        regions_breakdown: List[Dict],
        critical_violations: List[Dict]
    ) -> str:
        """
        Генерация текста обоснования в стиле документов комиссии
        """
        deviation = yield_details.get('deviation_from_standard', 0)
        regions_exceeding = yield_details.get('regions_exceeding', 0)
        regions_below = yield_details.get('regions_below', 0)

        # Получаем стандарт из первого региона
        standard_name = 'стандарт'
        if regions_breakdown:
            standard_name = regions_breakdown[0].get('standard_name', 'стандарт')

        # Выбираем репрезентативные регионы для примеров
        representative_regions = self._select_representative_regions(
            regions_breakdown, decision, max_count=2
        )

        # Генерация текста в зависимости от решения
        if decision == 'PROPOSE_TO_REGISTRY':
            text = self._generate_registry_justification(
                sort_name=sort_name,
                standard_name=standard_name,
                regions_exceeding=regions_exceeding,
                total_regions=total_regions,
                deviation=deviation,
                years_tested=years_tested,
                quality_score=quality_score,
                resistance_score=resistance_score,
                representative_regions=representative_regions,
                regions_breakdown=regions_breakdown
            )

        elif decision == 'PROPOSE_TO_REMOVE':
            text = self._generate_removal_justification(
                sort_name=sort_name,
                standard_name=standard_name,
                regions_exceeding=regions_exceeding,
                regions_below=regions_below,
                total_regions=total_regions,
                deviation=deviation,
                representative_regions=representative_regions,
                critical_violations=critical_violations,
                regions_breakdown=regions_breakdown
            )

        else:  # CONTINUE_TRIALS
            text = self._generate_continuation_justification(
                sort_name=sort_name,
                standard_name=standard_name,
                yield_details=yield_details,
                regions_exceeding=regions_exceeding,
                regions_below=regions_below,
                total_regions=total_regions,
                years_tested=years_tested,
                coverage_percent=coverage_percent
            )

        return text

    def _generate_registry_justification(
        self,
        sort_name: str,
        standard_name: str,
        regions_exceeding: int,
        total_regions: int,
        deviation: float,
        years_tested: int,
        quality_score: Optional[float],
        resistance_score: Optional[float],
        representative_regions: List[Dict],
        regions_breakdown: List[Dict]
    ) -> str:
        """Генерация обоснования для включения в реестр"""
        exceeding_percent = (regions_exceeding / total_regions * 100) if total_regions > 0 else 0

        # СПЕЦИАЛЬНЫЙ СЛУЧАЙ: Сорт испытывается сам с собой как стандарт
        if regions_breakdown and sort_name == standard_name:
            # Проверяем, что все отклонения близки к нулю
            all_near_zero = all(abs(r.get('deviation_percent', 0)) <= 1.0 for r in regions_breakdown)

            if all_near_zero:
                text = (
                    f"Сорт {sort_name} испытывался как стандарт во всех {total_regions} регионах, "
                    f"показав стабильные результаты на уровне эталона. "
                )

                text += f"Прошел полный цикл испытаний ({years_tested} года). "

                # Добавляем примеры регионов
                for i, region in enumerate(representative_regions[:2]):
                    region_name = region.get('region_name', 'Регион')
                    predecessor = region.get('predecessor', 'неизвестно')
                    std_yield = region.get('standard_average_yield', 0)
                    sort_yield = region.get('current_year_yield', 0)
                    dev_percent = region.get('deviation_percent', 0)

                    if i == 0:
                        text += f"В {region_name} "
                    else:
                        text += f"В {region_name} "

                    text += (
                        f"по предшественнику {predecessor}: "
                        f"стандарт {std_yield:.1f} ц/га, "
                        f"сорт {sort_yield:.1f} ц/га, "
                        f"отклонение {dev_percent:+.1f}%. "
                    )

                # Добавляем информацию о качестве и устойчивости
                if quality_score is not None and resistance_score is not None:
                    text += (
                        f"Показатели качества и устойчивости подтверждают его статус как стандарта "
                        f"({quality_score:.1f} и {resistance_score:.1f} балла соответственно). "
                    )
                elif quality_score is not None:
                    text += f"Показатели качества подтверждают его статус как стандарта ({quality_score:.1f} балла). "
                elif resistance_score is not None:
                    text += f"Показатели устойчивости подтверждают его статус как стандарта ({resistance_score:.1f} балла). "

                text += "Рекомендуется к включению в реестр как проверенный стандартный сорт."

                return text

        # ОБЫЧНЫЙ СЛУЧАЙ: Сорт превышает стандарт
        text = (
            f"Сорт {sort_name} превышает стандарт {standard_name} "
            f"в {regions_exceeding} из {total_regions} регионов ({exceeding_percent:.0f}%). "
        )

        # Вычисляем средневзвешенное процентное отклонение по урожайности стандарта
        if deviation > 0 and regions_breakdown:
            total_weight = 0
            weighted_sum = 0
            for region in regions_breakdown:
                standard_yield = region.get('standard_average_yield', 0)
                deviation_percent = region.get('deviation_percent', 0)
                if standard_yield and standard_yield > 0:
                    weighted_sum += deviation_percent * standard_yield
                    total_weight += standard_yield

            avg_deviation_percent = weighted_sum / total_weight if total_weight > 0 else 0
            if avg_deviation_percent > 0:
                text += f"Средний уровень урожайности на {avg_deviation_percent:.1f}% выше стандарта (средневзвешенное по урожайности). "
        elif deviation > 0:
            text += f"Среднее превышение составляет {deviation:+.1f}%. "

        text += f"Прошел полный цикл испытаний ({years_tested} года). "

        # Добавляем примеры регионов
        for i, region in enumerate(representative_regions):
            region_name = region.get('region_name', 'Регион')
            predecessor = region.get('predecessor', 'неизвестно')
            std_yield = region.get('standard_average_yield', 0)
            sort_yield = region.get('current_year_yield', 0)
            dev_percent = region.get('deviation_percent', 0)

            if i == 0:
                text += f"В {region_name} "
            else:
                text += f"В {region_name} "

            text += (
                f"по предшественнику {predecessor}: "
                f"стандарт {std_yield:.1f} ц/га, "
                f"сорт {sort_yield:.1f} ц/га, "
                f"отклонение {dev_percent:+.1f}%. "
            )

        # Добавляем информацию о качестве и устойчивости
        if quality_score is not None and resistance_score is not None:
            text += (
                f"Показатели качества и устойчивости в норме "
                f"({quality_score:.1f} и {resistance_score:.1f} балла соответственно)."
            )
        elif quality_score is not None:
            text += f"Показатели качества в норме ({quality_score:.1f} балла)."
        elif resistance_score is not None:
            text += f"Показатели устойчивости в норме ({resistance_score:.1f} балла)."

        return text

    def _generate_removal_justification(
        self,
        sort_name: str,
        standard_name: str,
        regions_exceeding: int,
        regions_below: int,
        total_regions: int,
        deviation: float,
        representative_regions: List[Dict],
        critical_violations: List[Dict],
        regions_breakdown: List[Dict]
    ) -> str:
        """Генерация обоснования для снятия с испытаний"""
        if regions_exceeding == 0 and total_regions > 0:
            text = f"Сорт {sort_name} уступает стандарту {standard_name} во всех {total_regions} регионах. "
        elif regions_below > regions_exceeding:
            text = (
                f"Сорт {sort_name} уступает стандарту {standard_name} "
                f"в {regions_below} из {total_regions} регионов. "
            )
        else:
            text = f"Сорт {sort_name} демонстрирует неудовлетворительные результаты. "

        # Добавляем примеры регионов с отрицательными отклонениями
        for i, region in enumerate(representative_regions[:2]):
            region_name = region.get('region_name', 'Регион')
            predecessor = region.get('predecessor', 'неизвестно')
            std_yield = region.get('standard_average_yield', 0)
            sort_yield = region.get('current_year_yield', 0)
            dev_percent = region.get('deviation_percent', 0)

            text += (
                f"В {region_name} по предшественнику {predecessor}: "
                f"стандарт {std_yield:.1f} ц/га, "
                f"сорт {sort_yield:.1f} ц/га, "
                f"отклонение {dev_percent:+.1f}%. "
            )

        # Добавляем информацию о критических нарушениях
        if critical_violations:
            text += "Выявлены критические недостатки: "
            violations_text = ", ".join([v.get('message', '') for v in critical_violations[:2]])
            text += violations_text.lower() + "."

        # Добавляем информацию об отклонении в процентах (если отрицательное)
        if deviation < 0:
            # Вычисляем средневзвешенное процентное отклонение по урожайности стандарта
            # Регионы с более высокой урожайностью стандарта имеют больший вес
            total_weight = 0
            weighted_sum = 0

            for region in regions_breakdown:
                standard_yield = region.get('standard_average_yield', 0)
                deviation_percent = region.get('deviation_percent', 0)
                if standard_yield and standard_yield > 0:
                    weighted_sum += deviation_percent * standard_yield
                    total_weight += standard_yield

            avg_deviation_percent = weighted_sum / total_weight if total_weight > 0 else 0

            if avg_deviation_percent < 0:
                text += f" Средний уровень урожайности на {abs(avg_deviation_percent):.1f}% ниже стандарта (средневзвешенное по урожайности)."

        return text

    def _deduplicate_regions_by_deviation(self, regions_breakdown: List[Dict]) -> Dict:
        """
        Дедупликация регионов по region_id с подсчетом превышений/снижений

        Если сорт тестировался в одном регионе с разными предшественниками,
        считаем регион как превышающий если хотя бы один предшественник превысил стандарт.

        Returns:
            Dict с ключами: exceeding (int), below (int), neutral (int), total (int)
        """
        # Группируем по region_id
        regions_by_id = {}
        for region in regions_breakdown:
            region_id = region.get('region_id')
            if not region_id:
                continue

            deviation = region.get('deviation_percent', 0)

            if region_id not in regions_by_id:
                regions_by_id[region_id] = {'deviations': []}

            regions_by_id[region_id]['deviations'].append(deviation)

        # Определяем статус каждого региона
        exceeding = 0
        below = 0
        neutral = 0

        for region_id, data in regions_by_id.items():
            # Если хотя бы один предшественник превысил - считаем регион как превышающий
            has_exceeding = any(d > 0 for d in data['deviations'])
            has_below = any(d < 0 for d in data['deviations'])

            if has_exceeding and not has_below:
                exceeding += 1
            elif has_below and not has_exceeding:
                below += 1
            elif has_exceeding and has_below:
                # Регион с противоречивыми результатами - берем среднее
                avg = sum(data['deviations']) / len(data['deviations'])
                if avg > 0:
                    exceeding += 1
                elif avg < 0:
                    below += 1
                else:
                    neutral += 1
            else:
                neutral += 1

        return {
            'exceeding': exceeding,
            'below': below,
            'neutral': neutral,
            'total': len(regions_by_id)
        }

    def _generate_continuation_justification(
        self,
        sort_name: str,
        standard_name: str,
        yield_details: Dict,
        regions_exceeding: int,
        regions_below: int,
        total_regions: int,
        years_tested: int,
        coverage_percent: float
    ) -> str:
        """Генерация обоснования для продолжения испытаний"""
        # Дедупликация регионов (учитываем разных предшественников)
        regions_breakdown = yield_details.get('regions_breakdown', [])
        deduplicated = self._deduplicate_regions_by_deviation(regions_breakdown)

        tested_regions = deduplicated['total']
        unique_exceeding = deduplicated['exceeding']
        unique_below = deduplicated['below']

        # Определяем характер результатов
        if unique_exceeding > 0 and unique_below > 0:
            # Есть и превышения и провалы - неоднозначно
            text = f"Сорт {sort_name} показывает неоднозначные результаты. "
            text += (
                f"Превышает стандарт {standard_name} в {unique_exceeding} регионах, "
                f"уступает в {unique_below}. "
            )
        elif unique_exceeding > 0:
            # Только превышает - хорошо, но данных мало
            text = f"Сорт {sort_name} демонстрирует положительные результаты. "
            text += f"Превышает стандарт {standard_name} в {unique_exceeding} из {tested_regions} регионов. "
        elif unique_below > 0:
            # Только уступает - плохо
            text = f"Сорт {sort_name} показывает недостаточные результаты. "
            text += f"Уступает стандарту {standard_name} в {unique_below} из {tested_regions} регионов. "
        else:
            # Нейтральные результаты
            text = f"Сорт {sort_name} показывает результаты на уровне стандарта {standard_name}. "

        # Вычисляем средневзвешенное процентное отклонение по урожайности стандарта
        if regions_breakdown:
            total_weight = 0
            weighted_sum = 0
            for region in regions_breakdown:
                standard_yield = region.get('standard_average_yield', 0)
                deviation_percent = region.get('deviation_percent', 0)
                if standard_yield and standard_yield > 0:
                    weighted_sum += deviation_percent * standard_yield
                    total_weight += standard_yield

            avg_deviation_percent = weighted_sum / total_weight if total_weight > 0 else 0
            if avg_deviation_percent > 0:
                text += f"Средний уровень урожайности на {avg_deviation_percent:.1f}% выше стандарта (средневзвешенное по урожайности). "
            elif avg_deviation_percent < 0:
                text += f"Средний уровень урожайности на {abs(avg_deviation_percent):.1f}% ниже стандарта (средневзвешенное по урожайности). "

        # Добавляем детальную информацию по всем регионам
        if regions_breakdown:
            # Дедупликация: группируем по region_id и берем среднее отклонение
            region_map = {}
            for region_data in regions_breakdown:
                region_id = region_data.get('region_id')
                if region_id not in region_map:
                    region_map[region_id] = {
                        'region_name': region_data.get('region_name', 'Регион'),
                        'predecessor': region_data.get('predecessor', 'неизвестно'),
                        'std_yield': region_data.get('standard_average_yield', 0),
                        'sort_yield': region_data.get('current_year_yield', 0),
                        'dev_percent': region_data.get('deviation_percent', 0),
                        'count': 1
                    }
                else:
                    # Если регион встречается с разными предшественниками, усредняем
                    existing = region_map[region_id]
                    existing['std_yield'] = (existing['std_yield'] * existing['count'] + region_data.get('standard_average_yield', 0)) / (existing['count'] + 1)
                    existing['sort_yield'] = (existing['sort_yield'] * existing['count'] + region_data.get('current_year_yield', 0)) / (existing['count'] + 1)
                    existing['dev_percent'] = (existing['dev_percent'] * existing['count'] + region_data.get('deviation_percent', 0)) / (existing['count'] + 1)
                    existing['count'] += 1
                    # Добавляем предшественников через запятую
                    pred = region_data.get('predecessor', 'неизвестно')
                    if pred not in existing['predecessor']:
                        existing['predecessor'] += f", {pred}"

            # Сортируем по deviation_percent
            sorted_regions = sorted(region_map.values(), key=lambda r: r['dev_percent'], reverse=True)

            # Показываем все регионы
            for region in sorted_regions:
                text += (
                    f"В {region['region_name']} (предшественник: {region['predecessor']}) "
                    f"стандарт {region['std_yield']:.1f} ц/га, "
                    f"сорт {region['sort_yield']:.1f} ц/га, "
                    f"отклонение {region['dev_percent']:+.1f}%. "
                )

        reasons = []

        if years_tested < 3:
            reasons.append(
                f"недостаточная продолжительность испытаний ({years_tested} года, требуется 3)"
            )

        if coverage_percent < 50:
            reasons.append(
                f"недостаточное покрытие регионов (протестировано {tested_regions} из {total_regions} ГСУ, {coverage_percent:.0f}%)"
            )

        if reasons:
            text += "Однако " + " и ".join(reasons) + ". "

        text += "Рекомендуется продолжить испытания для накопления данных."

        return text

    def _select_representative_regions(
        self,
        regions_breakdown: List[Dict],
        decision: str,
        max_count: int = 2
    ) -> List[Dict]:
        """
        Выбор репрезентативных регионов для примеров в обосновании

        Для РЕЕСТРА - регионы с наибольшим положительным отклонением
        Для СНЯТИЯ - регионы с наибольшим отрицательным отклонением
        Для ПРОДОЛЖЕНИЯ - микс положительных и отрицательных
        """
        if not regions_breakdown:
            return []

        if decision == 'PROPOSE_TO_REGISTRY':
            # Сортируем по убыванию отклонения (лучшие регионы)
            sorted_regions = sorted(
                regions_breakdown,
                key=lambda r: r.get('deviation_percent', 0),
                reverse=True
            )
            return sorted_regions[:max_count]

        elif decision == 'PROPOSE_TO_REMOVE':
            # Сортируем по возрастанию отклонения (худшие регионы)
            sorted_regions = sorted(
                regions_breakdown,
                key=lambda r: r.get('deviation_percent', 0)
            )
            return sorted_regions[:max_count]

        else:  # CONTINUE_TRIALS
            # Берем по одному лучшему и худшему
            if len(regions_breakdown) >= 2:
                best = max(regions_breakdown, key=lambda r: r.get('deviation_percent', 0))
                worst = min(regions_breakdown, key=lambda r: r.get('deviation_percent', 0))
                return [best, worst]
            else:
                return regions_breakdown[:max_count]

    def _extract_key_facts(
        self,
        decision: str,
        yield_details: Dict,
        quality_score: Optional[float],
        resistance_score: Optional[float],
        years_tested: int,
        coverage_percent: float,
        regions_exceeding: int,
        total_regions: int,
        violations: List[Dict]
    ) -> List[str]:
        """Извлечение ключевых фактов для отображения"""
        facts = []

        # Факты о статусе в реестре ООС (первым, т.к. это важная информация)
        # Проверяем все коды, связанные со статусом patents
        patents_codes = ['TESTING_PATENTS_STATUS', 'ARCHIVE_PATENTS_STATUS',
                        'UNKNOWN_PATENTS_STATUS', 'INVALID_PATENTS_STATUS']
        patents_violations = [v for v in violations if v.get('code') in patents_codes]

        if patents_violations:
            # Берем первое предупреждение о статусе
            violation = patents_violations[0]
            details = violation.get('details', {})
            status_display = details.get('status_display', 'Неизвестно')
            facts.append(f"Статус в реестре ООС: {status_display}")

        # Факты по урожайности
        exceeding_percent = (regions_exceeding / total_regions * 100) if total_regions > 0 else 0
        deviation = yield_details.get('deviation_from_standard', 0)

        if regions_exceeding > 0:
            facts.append(
                f"Превышает стандарт в {regions_exceeding} из {total_regions} регионов "
                f"({exceeding_percent:.0f}%)"
            )
        else:
            facts.append(f"Уступает стандарту во всех {total_regions} регионах")

        if deviation != 0:
            sign = "+" if deviation > 0 else ""
            facts.append(f"Среднее отклонение урожайности: {sign}{deviation:.1f}%")

        # Факты по качеству и устойчивости
        if quality_score is not None:
            quality_text = self._get_quality_text(quality_score)
            facts.append(f"Качество продукции: {quality_score:.1f}/5 ({quality_text})")

        if resistance_score is not None:
            resistance_text = self._get_resistance_text(resistance_score)
            facts.append(f"Устойчивость к болезням: {resistance_score:.1f}/5 ({resistance_text})")

        # Факты по длительности испытаний
        if years_tested < 3:
            facts.append(
                f"Недостаточная длительность испытаний: {years_tested} года из 3 требуемых"
            )
        else:
            facts.append(f"Испытывался {years_tested} года")

        # Факты по покрытию регионов
        # Вычисляем количество УНИКАЛЬНЫХ протестированных регионов (без дубликатов по предшественникам)
        regions_breakdown = yield_details.get('regions_breakdown', [])
        unique_region_ids = set(r.get('region_id') for r in regions_breakdown if r.get('region_id'))
        tested_regions = len(unique_region_ids)

        facts.append(
            f"Покрытие регионов: {coverage_percent:.0f}% ({tested_regions} из {total_regions} ГСУ)"
        )

        return facts

    def _extract_risk_factors(
        self,
        decision: str,
        violations: List[Dict],
        yield_score: Optional[float],
        years_tested: int,
        coverage_percent: float
    ) -> List[str]:
        """Извлечение факторов риска"""
        risk_factors = []

        # Только критические нарушения (warnings перенесены в key_facts)
        critical_violations = [v for v in violations if v.get('severity') == 'critical']
        for violation in critical_violations:
            risk_factors.append(violation.get('message', ''))

        # Дополнительные риски для решения о включении в реестр
        if decision == 'PROPOSE_TO_REGISTRY':
            if years_tested < 3:
                risk_factors.append('Недостаточная продолжительность испытаний')
            if coverage_percent < 50:
                risk_factors.append(f'Низкое покрытие регионов ({coverage_percent:.0f}%)')

        return risk_factors

    def _get_quality_text(self, score: float) -> str:
        """Текстовая оценка качества"""
        if score >= 4.5:
            return "отличное"
        elif score >= 3.5:
            return "хорошее"
        elif score >= 2.5:
            return "удовлетворительное"
        else:
            return "низкое"

    def _get_resistance_text(self, score: float) -> str:
        """Текстовая оценка устойчивости"""
        if score >= 4.5:
            return "отличная"
        elif score >= 3.5:
            return "хорошая"
        elif score >= 2.5:
            return "удовлетворительная"
        else:
            return "низкая"
