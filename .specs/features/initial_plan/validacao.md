# Validações pré-entrega (geradas por check_plan.py — não editar à mão)

## Mapa de ondas (calculado)

| Onda | Tasks | Risco máx | Gatilhos previstos | QA previsto |
|---|---|---|---|---|
| 1 | TASK-001 | baixo | — | — |
| 2 | TASK-002, TASK-011 | médio | — | — |
| 3 | TASK-003 | crítico | G1 TASK-003 | EXAUSTIVO |
| 4 | TASK-025 | alto | G1 TASK-025 | RIGOROSO |
| 5 | TASK-045 | alto | G1 TASK-045 | RIGOROSO |
| 6 | TASK-004, TASK-016, TASK-026, TASK-046 | médio | — | — |
| 7 | TASK-005 | crítico | G1 TASK-005 | EXAUSTIVO |
| 8 | TASK-006 | crítico | G1 TASK-006 | EXAUSTIVO |
| 9 | TASK-007 | crítico | G1 TASK-007 | EXAUSTIVO |
| 10 | TASK-008, TASK-017, TASK-027 | médio | G2 CT-3 | PADRAO |
| 11 | TASK-018 | alto | G1 TASK-018 | RIGOROSO |
| 12 | TASK-019 | alto | G1 TASK-019 | RIGOROSO |
| 13 | TASK-009, TASK-020, TASK-033, TASK-034 | médio | G2 CT-11,CT-13 | PADRAO |
| 14 | TASK-038 | crítico | G1 TASK-038 | EXAUSTIVO |
| 15 | TASK-039 | crítico | G1 TASK-039 | EXAUSTIVO |
| 16 | TASK-010, TASK-012, TASK-021, TASK-041 | médio | G2 CT-7 | PADRAO |
| 17 | TASK-028 | alto | G1 TASK-028; G3 (1 história(s) P1) | RIGOROSO |
| 18 | TASK-035 | alto | G1 TASK-035 | RIGOROSO |
| 19 | TASK-013, TASK-022, TASK-029, TASK-047 | médio | G2 CT-19,CT-20; G3 (1 história(s) P1) | PADRAO |
| 20 | TASK-048 | alto | G1 TASK-048 | RIGOROSO |
| 21 | TASK-049 | crítico | G1 TASK-049 | EXAUSTIVO |
| 22 | TASK-014, TASK-023, TASK-030, TASK-051 | médio | G2 CT-9,CT-20; G3 (3 história(s) P1) | PADRAO |
| 23 | TASK-052 | alto | G1 TASK-052 | RIGOROSO |
| 24 | TASK-015, TASK-036, TASK-053 | médio | — | — |
| 25 | TASK-024, TASK-042 | médio | G3 (1 história(s) P1) | PADRAO |
| 26 | TASK-031, TASK-054 | médio | G3 (1 história(s) P1) | PADRAO |
| 27 | TASK-032, TASK-055 | médio | G3 (2 história(s) P1) | PADRAO |
| 28 | TASK-037, TASK-040 | médio | G2 CT-9; G3 (2 história(s) P1) | PADRAO |
| 29 | TASK-043, TASK-050 | médio | G2 CT-9 | PADRAO |
| 30 | TASK-044 | médio | — | — |

PRs previstos (uma fase termina numa onda com QA semântico; a última, no QA FEATURE): fase 1: ondas 1, 2, 3 · fase 2: ondas 4 · fase 3: ondas 5 · fase 4: ondas 6, 7 · fase 5: ondas 8 · fase 6: ondas 9 · fase 7: ondas 10 · fase 8: ondas 11 · fase 9: ondas 12 · fase 10: ondas 13 · fase 11: ondas 14 · fase 12: ondas 15 · fase 13: ondas 16 · fase 14: ondas 17 · fase 15: ondas 18 · fase 16: ondas 19 · fase 17: ondas 20 · fase 18: ondas 21 · fase 19: ondas 22 · fase 20: ondas 23 · fase 21: ondas 24, 25 · fase 22: ondas 26 · fase 23: ondas 27 · fase 24: ondas 28 · fase 25: ondas 29 · fase 26: ondas 30

Caminho crítico: TASK-001 → TASK-002 → TASK-003 → TASK-004 → TASK-008 → TASK-018 → TASK-020 → TASK-021 → TASK-028 → TASK-029 → TASK-030 → TASK-031 → TASK-032 → TASK-037 (14 tasks)
G4 (gate cego) e G5 (retry) só são conhecidos na execução.

## Cobertura de requisitos

| ID do spec | Task(s) | Status |
|---|---|---|
| `JC-60` | TASK-006, TASK-007, TASK-013 | ✅ |
| `JC-61` | TASK-005, TASK-007, TASK-012, TASK-013 | ✅ |
| `JC-62` | TASK-003, TASK-004, TASK-005, TASK-017, TASK-030 | ✅ |
| `JC-63` | TASK-005, TASK-007, TASK-012, TASK-014 | ✅ |
| `JC-64` | TASK-038, TASK-040, TASK-052 | ✅ |
| `JC-65` | TASK-019, TASK-047, TASK-052, TASK-053 | ✅ |
| `JC-66` | TASK-010, TASK-015 | ✅ |
| `JC-67` | TASK-005, TASK-010, TASK-015, TASK-047 | ✅ |
| `JC-68` | TASK-010, TASK-015 | ✅ |
| `JC-69` | TASK-006, TASK-007, TASK-013 | ✅ |
| `JC-77` | TASK-039, TASK-040 | ✅ |
| `JC-70` | TASK-016, TASK-017, TASK-020, TASK-021, TASK-022, TASK-024 | ✅ |
| `JC-71` | TASK-016, TASK-018, TASK-020, TASK-028, TASK-035 | ✅ |
| `JC-72` | TASK-020 | ✅ |
| `JC-73` | TASK-021, TASK-023, TASK-024 | ✅ |
| `JC-74` | TASK-021, TASK-023 | ✅ |
| `JC-75` | TASK-021 | ✅ |
| `JC-76` | TASK-021, TASK-022, TASK-024 | ✅ |
| `JC-78` | TASK-016, TASK-022, TASK-024 | ✅ |
| `JC-79` | TASK-016, TASK-022, TASK-024 | ✅ |
| `JC-01` | TASK-025, TASK-027, TASK-030 | ✅ |
| `JC-02` | TASK-018, TASK-028 | ✅ |
| `JC-03` | TASK-018, TASK-027, TASK-028 | ✅ |
| `JC-04` | TASK-019, TASK-028, TASK-032 | ✅ |
| `JC-05` | TASK-026, TASK-028 | ✅ |
| `JC-06` | TASK-026, TASK-032 | ✅ |
| `JC-07` | TASK-026, TASK-032 | ✅ |
| `JC-08` | TASK-027, TASK-028, TASK-032 | ✅ |
| `JC-09` | TASK-029, TASK-030, TASK-031 | ✅ |
| `JC-16` | TASK-029, TASK-030, TASK-032 | ✅ |
| `JC-17` | TASK-004, TASK-025, TASK-029, TASK-030, TASK-031 | ✅ |
| `JC-18` | TASK-028, TASK-032 | ✅ |
| `JC-19` | TASK-008, TASK-009, TASK-014, TASK-028, TASK-035 | ✅ |
| `JC-10` | TASK-034, TASK-035 | ✅ |
| `JC-11` | TASK-033, TASK-035 | ✅ |
| `JC-12` | TASK-033, TASK-035 | ✅ |
| `JC-13` | TASK-033, TASK-035, TASK-037 | ✅ |
| `JC-14` | TASK-017, TASK-035, TASK-036, TASK-037 | ✅ |
| `JC-15` | TASK-035 | ✅ |
| `JC-55` | TASK-035, TASK-036, TASK-037 | ✅ |
| `JC-56` | TASK-034, TASK-035 | ✅ |
| `JC-20` | TASK-041, TASK-042, TASK-044 | ✅ |
| `JC-21` | TASK-041 | ✅ |
| `JC-22` | TASK-041 | ✅ |
| `JC-23` | TASK-029, TASK-031, TASK-041, TASK-044 | ✅ |
| `JC-24` | TASK-041, TASK-042, TASK-043 | ✅ |
| `JC-25` | TASK-041, TASK-042, TASK-043 | ✅ |
| `JC-30` | TASK-045, TASK-046, TASK-047, TASK-048, TASK-049 | ✅ |
| `JC-31` | TASK-027, TASK-047 | ✅ |
| `JC-32` | TASK-047 | ✅ |
| `JC-33` | TASK-047 | ✅ |
| `JC-34` | TASK-048, TASK-050 | ✅ |
| `JC-35` | TASK-047 | ✅ |
| `JC-40` | TASK-051, TASK-052, TASK-054 | ✅ |
| `JC-41` | TASK-052 | ✅ |
| `JC-42` | TASK-052, TASK-053, TASK-055 | ✅ |
| `JC-43` | TASK-029, TASK-031, TASK-055 | ✅ |
| `JC-44` | TASK-052 | ✅ |
| `JC-45` | TASK-052, TASK-053 | ✅ |
| `JC-50` | TASK-031, TASK-047 | ✅ |
| `JC-52` | TASK-029, TASK-030, TASK-032 | ✅ |
| `JC-53` | TASK-009, TASK-040, TASK-047 | ✅ |
| `JC-54` | TASK-009, TASK-014 | ✅ |
| `JC-46` | TASK-003, TASK-009, TASK-040 | ✅ |
| `JC-80` | TASK-025, TASK-030, TASK-031 | ✅ |
| `JC-81` | TASK-031 | ✅ |
| `JC-82` | TASK-028 | ✅ |
| `JC-83` | TASK-018, TASK-020, TASK-026, TASK-028 | ✅ |
| `JC-84` | TASK-028, TASK-029 | ✅ |
| `JC-85` | TASK-021, TASK-029, TASK-031, TASK-035 | ✅ |
| `JC-87` | TASK-028, TASK-029, TASK-032 | ✅ |
| `JC-88` | TASK-025, TASK-028, TASK-032 | ✅ |
| `JC-89` | TASK-047 | ✅ |
| `JC-91` | TASK-004, TASK-027, TASK-029 | ✅ |
| `JC-92` | TASK-047, TASK-048 | ✅ |
| `JC-93` | TASK-052, TASK-054, TASK-055 | ✅ |
| `JC-94` | TASK-052 | ✅ |
| `JC-95` | TASK-047 | ✅ |
| `JC-96` | TASK-001, TASK-002, TASK-005, TASK-011, TASK-012, TASK-030 | ✅ |
| `JC-97` | TASK-018, TASK-028 | ✅ |
| `JC-98` | TASK-016, TASK-022, TASK-024 | ✅ |
| `JC-99` | TASK-003, TASK-008, TASK-010, TASK-014, TASK-028, TASK-035 | ✅ |
| `JC-57` | TASK-017, TASK-019, TASK-029, TASK-030 | ✅ |
| `JC-58` | TASK-028 | ✅ |
| `JC-59` | TASK-008 | ✅ |

Cobertura: 85/85

## Dependências

| Task | Depende de | Onda | Ondas das dependências |
|---|---|---|---|
| TASK-001 | — | 1 | — |
| TASK-002 | TASK-001 | 2 | 1 |
| TASK-003 | TASK-002 | 3 | 2 |
| TASK-004 | TASK-003 | 6 | 3 |
| TASK-005 | TASK-004 | 7 | 6 |
| TASK-006 | TASK-004 | 8 | 6 |
| TASK-007 | TASK-005, TASK-006 | 9 | 7, 8 |
| TASK-008 | TASK-004 | 10 | 6 |
| TASK-009 | TASK-005, TASK-008 | 13 | 7, 10 |
| TASK-010 | TASK-005, TASK-006, TASK-008 | 16 | 7, 8, 10 |
| TASK-011 | TASK-001 | 2 | 1 |
| TASK-012 | TASK-007, TASK-009, TASK-011 | 16 | 9, 13, 2 |
| TASK-013 | TASK-012 | 19 | 16 |
| TASK-014 | TASK-012 | 22 | 16 |
| TASK-015 | TASK-010, TASK-012 | 24 | 16, 16 |
| TASK-016 | TASK-003 | 6 | 3 |
| TASK-017 | TASK-004 | 10 | 6 |
| TASK-018 | TASK-008, TASK-016 | 11 | 10, 6 |
| TASK-019 | TASK-003, TASK-008 | 12 | 3, 10 |
| TASK-020 | TASK-016, TASK-018 | 13 | 6, 11 |
| TASK-021 | TASK-008, TASK-017, TASK-019, TASK-020 | 16 | 10, 10, 12, 13 |
| TASK-022 | TASK-005, TASK-021 | 19 | 7, 16 |
| TASK-023 | TASK-012, TASK-022 | 22 | 16, 19 |
| TASK-024 | TASK-023 | 25 | 22 |
| TASK-025 | TASK-003 | 4 | 3 |
| TASK-026 | TASK-002 | 6 | 2 |
| TASK-027 | TASK-004 | 10 | 6 |
| TASK-028 | TASK-008, TASK-018, TASK-019, TASK-020, TASK-021, TASK-025, TASK-026, TASK-027 | 17 | 10, 11, 12, 13, 16, 4, 6, 10 |
| TASK-029 | TASK-017, TASK-019, TASK-025, TASK-027, TASK-028 | 19 | 10, 12, 4, 10, 17 |
| TASK-030 | TASK-005, TASK-029 | 22 | 7, 19 |
| TASK-031 | TASK-012, TASK-030 | 26 | 16, 22 |
| TASK-032 | TASK-031 | 27 | 26 |
| TASK-033 | TASK-016, TASK-018, TASK-026 | 13 | 6, 11, 6 |
| TASK-034 | TASK-016, TASK-018 | 13 | 6, 11 |
| TASK-035 | TASK-008, TASK-017, TASK-018, TASK-021, TASK-027, TASK-033, TASK-034 | 18 | 10, 10, 11, 16, 10, 13, 13 |
| TASK-036 | TASK-005, TASK-035 | 24 | 7, 18 |
| TASK-037 | TASK-032, TASK-036 | 28 | 27, 24 |
| TASK-038 | TASK-005, TASK-009, TASK-017, TASK-019 | 14 | 7, 13, 10, 12 |
| TASK-039 | TASK-009, TASK-017 | 15 | 13, 10 |
| TASK-040 | TASK-009, TASK-012, TASK-038, TASK-039 | 28 | 13, 16, 14, 15 |
| TASK-041 | TASK-027 | 16 | 10 |
| TASK-042 | TASK-005, TASK-041 | 25 | 7, 16 |
| TASK-043 | TASK-012, TASK-042 | 29 | 16, 25 |
| TASK-044 | TASK-032, TASK-043 | 30 | 27, 29 |
| TASK-045 | TASK-025 | 5 | 4 |
| TASK-046 | TASK-045 | 6 | 5 |
| TASK-047 | TASK-008, TASK-027, TASK-028, TASK-046 | 19 | 10, 10, 17, 6 |
| TASK-048 | TASK-005, TASK-047 | 20 | 7, 19 |
| TASK-049 | TASK-048 | 21 | 20 |
| TASK-050 | TASK-012, TASK-040, TASK-048 | 29 | 16, 28, 20 |
| TASK-051 | TASK-027, TASK-028 | 22 | 10, 17 |
| TASK-052 | TASK-038, TASK-041, TASK-051 | 23 | 14, 16, 22 |
| TASK-053 | TASK-027, TASK-052 | 24 | 10, 23 |
| TASK-054 | TASK-005, TASK-052, TASK-053 | 26 | 7, 23, 24 |
| TASK-055 | TASK-031, TASK-054 | 27 | 26, 26 |

## Contratos (produtor × consumidores)

| Contrato | Produtor | Consumidores |
|---|---|---|
| CT-1 | TASK-003 | TASK-005, TASK-016, TASK-025 |
| CT-2 | TASK-003 | TASK-004, TASK-006, TASK-018, TASK-019 |
| CT-3 | TASK-004 | TASK-005, TASK-006, TASK-008, TASK-017, TASK-027, TASK-038, TASK-039 |
| CT-4 | TASK-005 | TASK-007, TASK-009, TASK-010, TASK-022, TASK-030, TASK-036, TASK-042, TASK-048, TASK-054 |
| CT-5 | TASK-005 | TASK-007, TASK-010, TASK-038 |
| CT-6 | TASK-006 | TASK-007, TASK-010 |
| CT-7 | TASK-008 | TASK-009, TASK-010, TASK-021, TASK-028, TASK-035, TASK-047 |
| CT-8 | TASK-009 | TASK-012, TASK-014, TASK-040 |
| CT-9 | TASK-012 | TASK-013, TASK-014, TASK-015, TASK-023, TASK-031, TASK-037, TASK-040, TASK-043, TASK-050, TASK-055 |
| CT-10 | TASK-017 | TASK-021, TASK-029, TASK-035, TASK-038, TASK-039 |
| CT-11 | TASK-018 | TASK-020, TASK-028, TASK-033, TASK-034, TASK-035 |
| CT-12 | TASK-019 | TASK-021, TASK-028, TASK-029, TASK-038 |
| CT-13 | TASK-016 | TASK-018, TASK-020, TASK-021, TASK-033, TASK-034 |
| CT-14 | TASK-020 | TASK-021, TASK-028 |
| CT-15 | TASK-021 | TASK-022, TASK-028, TASK-035 |
| CT-16 | TASK-022 | TASK-023, TASK-024 |
| CT-17 | TASK-025 | TASK-028, TASK-029, TASK-045 |
| CT-18 | TASK-026 | TASK-028, TASK-033 |
| CT-19 | TASK-027 | TASK-028, TASK-029, TASK-035, TASK-041, TASK-047, TASK-051, TASK-053 |
| CT-20 | TASK-028 | TASK-029, TASK-030, TASK-047, TASK-051 |
| CT-21 | TASK-029 | TASK-030 |
| CT-22 | TASK-030 | TASK-031, TASK-032 |
| CT-23 | TASK-033 | TASK-035 |
| CT-24 | TASK-034 | TASK-035 |
| CT-25 | TASK-035 | TASK-036 |
| CT-26 | TASK-036 | TASK-037 |
| CT-27 | TASK-038 | TASK-052 |
| CT-28 | TASK-039 | — |
| CT-29 | TASK-041 | TASK-042, TASK-052 |
| CT-30 | TASK-042 | TASK-043, TASK-044 |
| CT-31 | TASK-045 | TASK-046, TASK-047, TASK-048 |
| CT-32 | TASK-047 | TASK-048 |
| CT-33 | TASK-048 | TASK-049 |
| CT-34 | TASK-048 | TASK-050 |
| CT-35 | TASK-051 | TASK-052, TASK-053 |
| CT-36 | TASK-052 | TASK-053, TASK-054 |
| CT-37 | TASK-053 | TASK-054 |
| CT-38 | TASK-054 | TASK-055 |
| CT-39 | TASK-010 | TASK-015 |
| CT-40 | TASK-007 | TASK-012, TASK-013 |

## Granularidade e testes

| Task | Produção | Teste | Testes | Paralelo-seguro | Agente |
|---|---|---|---|---|---|
| TASK-001 | 2 | 0 | none | sim | hm-engineer |
| TASK-002 | 2 | 1 | integration | sim | hm-engineer |
| TASK-003 | 2 | 2 | unit | sim | hm-engineer |
| TASK-004 | 1 | 2 | integration | sim | hm-engineer |
| TASK-005 | 2 | 3 | integration | sim | hm-engineer |
| TASK-006 | 1 | 1 | integration | sim | hm-engineer |
| TASK-007 | 2 | 1 | integration | sim | hm-engineer |
| TASK-008 | 2 | 2 | integration | sim | hm-engineer |
| TASK-009 | 2 | 1 | integration | sim | hm-engineer |
| TASK-010 | 2 | 1 | integration | sim | hm-engineer |
| TASK-011 | 2 | 1 | unit | sim | hm-designer |
| TASK-012 | 2 | 2 | unit | sim | hm-designer |
| TASK-013 | 2 | 2 | unit | sim | hm-designer |
| TASK-014 | 1 | 1 | unit | sim | hm-designer |
| TASK-015 | 2 | 2 | unit | sim | hm-designer |
| TASK-016 | 2 | 3 | unit | sim | hm-engineer |
| TASK-017 | 1 | 1 | integration | sim | hm-engineer |
| TASK-018 | 2 | 4 | unit | não | hm-engineer |
| TASK-019 | 2 | 3 | unit | não | hm-engineer |
| TASK-020 | 2 | 2 | unit | sim | hm-engineer |
| TASK-021 | 1 | 1 | integration | sim | hm-engineer |
| TASK-022 | 1 | 2 | integration | sim | hm-engineer |
| TASK-023 | 2 | 2 | unit | sim | hm-designer |
| TASK-024 | 1 | 1 | unit | sim | hm-designer |
| TASK-025 | 2 | 3 | unit | sim | hm-engineer |
| TASK-026 | 2 | 2 | unit | sim | hm-engineer |
| TASK-027 | 2 | 1 | integration | sim | hm-engineer |
| TASK-028 | 2 | 2 | integration | sim | hm-engineer |
| TASK-029 | 1 | 1 | integration | sim | hm-engineer |
| TASK-030 | 1 | 1 | integration | sim | hm-engineer |
| TASK-031 | 2 | 2 | unit | sim | hm-designer |
| TASK-032 | 2 | 2 | unit | sim | hm-designer |
| TASK-033 | 1 | 1 | unit | sim | hm-engineer |
| TASK-034 | 1 | 1 | unit | sim | hm-engineer |
| TASK-035 | 1 | 1 | integration | sim | hm-engineer |
| TASK-036 | 1 | 1 | integration | sim | hm-engineer |
| TASK-037 | 2 | 2 | unit | sim | hm-designer |
| TASK-038 | 1 | 1 | integration | sim | hm-engineer |
| TASK-039 | 1 | 1 | integration | sim | hm-engineer |
| TASK-040 | 2 | 2 | unit | sim | hm-designer |
| TASK-041 | 2 | 2 | integration | sim | hm-engineer |
| TASK-042 | 1 | 1 | integration | sim | hm-engineer |
| TASK-043 | 2 | 2 | unit | sim | hm-designer |
| TASK-044 | 1 | 1 | unit | sim | hm-designer |
| TASK-045 | 2 | 3 | unit | sim | hm-engineer |
| TASK-046 | 1 | 2 | unit | sim | hm-engineer |
| TASK-047 | 2 | 1 | integration | sim | hm-engineer |
| TASK-048 | 2 | 1 | integration | sim | hm-engineer |
| TASK-049 | 2 | 1 | unit | sim | hm-engineer |
| TASK-050 | 2 | 2 | unit | sim | hm-designer |
| TASK-051 | 1 | 1 | unit | sim | hm-engineer |
| TASK-052 | 2 | 3 | unit | sim | hm-engineer |
| TASK-053 | 1 | 1 | integration | sim | hm-engineer |
| TASK-054 | 1 | 1 | integration | sim | hm-engineer |
| TASK-055 | 2 | 2 | unit | sim | hm-designer |
