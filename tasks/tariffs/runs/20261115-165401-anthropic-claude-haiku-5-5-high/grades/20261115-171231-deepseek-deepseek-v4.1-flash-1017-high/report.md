# Grading report

Submission: `/mnt/workspace/f1-research-benchmark/tasks/tariffs/runs/20261115-165401-anthropic-claude-haiku-5-5-high/answer.md`

**Score: 62.50 / 100** (unclear counted as no; range 62.50 to 62.50)

## Rubric feedback

1) q10f_surcharge requires 'the proclamation number or the document number' and refuses credit to an answer that identifies the instrument as '91 FR 9339, clause (1)'. That is a first-page FR citation to Proclamation 11012 and at least as traceable as the identifiers named; the rubric elsewhere (e.g. q2a_basis: 'FR Doc. 2026-17294 or 91 FR 54790') accepts the two interchangeably, so this criterion is inconsistent and arguably should accept a correct FR citation. 2) q14_3_jordan silently requires the list of six economies that imposed bans on top of the Jordan point; a submission that explains only Jordan's own basis (an accurate answer to the statement's main error) loses the point on an element it could not know was separately scored. Consider marking that clause 'welcome but not required'. 3) q1_dairy_xref and q4c_xref both test the same single sentence of Proclamation 11062(3), so one omission costs points twice on different questions. 4) Q15 concentrates 14 criteria on a single interpretive fork (whether the Canada IEEPA duties survived and how Executive Order 14289 orders the two duties); a submission that gets the ordering backwards loses almost the whole question, which is by design but makes Q15 a very low-information discriminator. 5) The Q11 do-not-count note on 'Proclamation 11056's suspension against its change of the effective date' sits close to a genuinely arguable discrepancy (the unconditional operative date against recitals attributing the lapse to Canada's August 21 conduct); a line explaining that the recitals describe rather than contradict the operative text would make the instruction clearer.

| Question | Score | Max | Range |
|---|---|---|---|
| Q1 | 1.89 | 2 | 1.89 to 1.89 |
| Q2 | 3.00 | 3 | 3.00 to 3.00 |
| Q3 | 3.00 | 3 | 3.00 to 3.00 |
| Q4 | 3.64 | 4 | 3.64 to 3.64 |
| Q5 | 3.00 | 3 | 3.00 to 3.00 |
| Q6 | 3.00 | 3 | 3.00 to 3.00 |
| Q7 | 1.00 | 1 | 1.00 to 1.00 |
| Q8 | 2.00 | 2 | 2.00 to 2.00 |
| Q9 | 2.72 | 3 | 2.72 to 2.72 |
| Q10 | 2.40 | 3 | 2.40 to 2.40 |
| Q11 | 4.00 | 25 | 4.00 to 4.00 |
| Q12 | 1.17 | 4 | 1.17 to 1.17 |
| Q13 | 19.00 | 19 | 19.00 to 19.00 |
| Q14 | 8.40 | 10 | 8.40 to 8.40 |
| Q15 | 4.29 | 15 | 4.29 to 4.29 |

## Q1: 1.89 / 2

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q1_duty_procs` | credit | yes | 0.3333 (of 0.333333) | Lists 11046 (2026-14991), 11047 (2026-14992), 11048 (2026-14997), each 'signed July 20, published July 23, 2026' — all correct. |
| `q1_details` | credit | yes | 0.2222 (of 0.222222) | All ten documents carry correct first pages (46639, 46653, 46663, 54789, 58311, 58319, 58325, 58331, 58339, 68861) and a correct one-line description; extra filing details (11056 'Filed 8-21-26; 11:15 am', 11061 'Filed 9-11-26') were checked and are accurate. |
| `q1_delay` | credit | yes | 0.2222 (of 0.222222) | 'Proclamation 11056, FR Doc 2026-17294, 91 FR 54789, signed August 18 ... published August 24 ... sets the effective date at 12:01 a.m. August 22, 2026', correctly framed as moving the Aug. 19 date set in 11046-11048. |
| `q1_exclusions` | credit | yes | 0.3333 (of 0.333333) | All three (11061/2026-18835, 11062/2026-18836, 11063/2026-18837; 91 FR 58311/58319/58325), signed Sept. 8, published Sept. 14, operative 'imported on or after 12:01 a.m. September 29, 2026'. |
| `q1_scope` | credit | yes | 0.3333 (of 0.333333) | 11064 (2026-18838) and 11065 (2026-18839) signed Sept. 8, effective 12:01 a.m. Sept. 15; 11076 (2026-22292) signed Oct. 23, published Oct. 30, effective 12:01 a.m. Oct. 30. All operative dates correct. |
| `q1_events` | credit | yes | 0.2222 (of 0.222222) | Each duty/scope item is labelled 'entry event' or 'entry/withdrawal event', and each exclusion is labelled 'an import/arrival event' with clause (1) of 11061 cited. |
| `q1_dairy_none` | credit | yes | 0.2222 (of 0.222222) | States 'Dairy: 11047 set the original Annex II; no scope proclamation for dairy was found', while attributing the alcohol change to 11064 and the motor-vehicle changes to 11065 and 11076. |
| `q1_dairy_xref` | credit | no | 0 | The phantom September 8 dairy scope proclamation cited in Proclamation 11062 clause (3) is never mentioned anywhere in the submission. |
| `q1_cite` | penalty | no | 0 | Penalty not applicable: nearly every factual claim carries a document number and FR page or clause citation. |
| `q1_fab` | penalty | no | 0 | Penalty not applicable: the non-key details (11056 and 11061 filing legends) were verified with fr_grep and are accurate; no invented source. |

## Q2: 3.00 / 3

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q2a_zero` | credit | yes | 0.375 | 'Entry 1 (2:00 p.m. August 20): $0. Entry 2 (11:59 p.m. August 21): $0.' |
| `q2a_third` | credit | yes | 0.375 | 'Entry 3 (12:01 a.m. August 22): 50% x $40,000 = $20,000'. |
| `q2a_basis` | credit | yes | 0.1875 | Relies on clause (1) of 11056 (2026-17294) resetting the effective date to 12:01 a.m. Aug. 22, 2026, plus clause (1) of 11046; 91 FR 54790 given in the basis field. |
| `q2b_chapeau` | credit | yes | 0.375 | 'Clauses (1) and (3) of 11046 still print "August 19, 2026" in the body ... the amendment is textually limited to the chapeau; the body clauses were not amended.' |
| `q2b_resolve` | credit | yes | 0.375 | 'The resolution is clause (1) of 11056, which is the later and specific text', with later recitals confirming Aug. 22 — one of the accepted routes. |
| `q2c_refund` | credit | yes | 0.375 | Quotes clause (4) of 11056 (91 FR 54791): refunds 'processed under applicable law and CBP's standard procedures'; adds that no timing, interest or claim mechanism is given. |
| `q2d_no_action` | credit | yes | 0.2812 (of 0.28125) | Says no further presidential action was needed and cites the recitals of 11064 (and 11065/11076) that at 12:01 a.m. Aug. 22 'the 3-day suspension lapsed and the duties became effective'. |
| `q2d_reneged` | credit | yes | 0.2812 (of 0.28125) | 'on August 21 Canada reneged' per the recitals of the September 8 proclamations (11064/11065, 91 FR 58331/58339); the Aug. 21 date and the reneging are both given. |
| `q2e_thirty` | credit | yes | 0.375 | July 20 + 30 days = August 19, arithmetic shown, with recital 10 of 11046 (91 FR 46641) quoted for the 30-day rule. |
| `q2_cite` | penalty | no | 0 | Penalty not applicable: document numbers, clauses and pages are cited throughout. |
| `q2_fab` | penalty | no | 0 | Penalty not applicable: the '11056 filed August 21, 2026 at 11:15 a.m.' claim was verified against the document footer and is correct. |

## Q3: 3.00 / 3

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q3a_shipment_a` | credit | yes | 0.15 | May be imported; 50% x $30,000 = $15,000. |
| `q3a_shipment_b` | credit | yes | 0.45 (of 0.45) | Not excluded (imported Sept. 27); $15,000 on the Oct. 5 withdrawal under clause (2) of 11061. |
| `q3a_shipment_c` | credit | yes | 0.45 (of 0.45) | Not excluded because 11:30 p.m. Sept. 28 importation precedes the cutoff; entry Sept. 29 at 50% = $15,000. |
| `q3a_shipment_d` | credit | yes | 0.45 (of 0.45) | Excluded from importation (arrival 12:30 a.m. Sept. 29, clause (1) of 11061); 'no consumption entry is possible'. |
| `q3b_result` | credit | yes | 0.45 (of 0.45) | Not excluded; 50% x $30,000 = $15,000 on entry from the zone Oct. 6 under clause (2) of 11061. |
| `q3b_ftz` | credit | yes | 0.3 | Cites 11046 clause (4): privileged foreign status and duty on entry for consumption. |
| `q3c_invalid` | credit | yes | 0.45 (of 0.45) | The 50% duty of 11046 applies under 11061 clause (9)(b) (91 FR 58313). |
| `q3d_no_change` | credit | yes | 0.3 | No; clause (3) of 11061 'does not otherwise affect' products subject to 11046, so unlisted products stay at 50%. |
| `q3_cite` | penalty | no | 0 | Penalty not applicable: provision-level citations throughout. |
| `q3_fab` | penalty | no | 0 | Penalty not applicable: no invented sources; the 11061 filing date checked out. |

## Q4: 3.64 / 4

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q4a_amounts` | credit | yes | 0.7273 (of 0.727273) | Sept. 10: $25,000 section 232 and $0 section 338 for X, Y and Z. |
| `q4a_basis` | credit | yes | 0.3636 (of 0.363636) | Rests on clause (2) of 11046/11047/11048 ('shall not apply to articles subject to duties pursuant to section 232', 46641/46655/46665), not on the duties not yet having started. |
| `q4b_x` | credit | yes | 0.5455 (of 0.545455) | $25,000 + 50% x $100,000 = $50,000 via clause (1) of 11064 effective Sept. 15. |
| `q4b_z` | credit | yes | 0.5455 (of 0.545455) | $25,000 + $50,000 via the same stacking sentence in clause (1) of 11065. |
| `q4b_y` | credit | yes | 0.7273 (of 0.727273) | $25,000 + $0, because no dairy scope modification exists and clause (2) of 11047 still applies. |
| `q4c_text` | credit | yes | 0.5455 (of 0.545455) | Identifies both the clause (2) carve-outs (46641/46655/46665) and the 'in addition to duties imposed pursuant to section 232' sentence in 11064 (58332) and 11065 (58340), effective Sept. 15. |
| `q4c_supersede` | credit | yes | 0.1818 (of 0.181818) | Uncertainty field notes the later proclamations do not expressly amend clause (2) but that 'the later text is the more specific and the only operative statement on section 232 for the post-September 15 period' — i.e. the later clause displaces clause (2) from Sept. 15, an accepted route. |
| `q4c_xref` | credit | no | 0 | 11062 clause (3)'s reference to a nonexistent dairy scope proclamation is not mentioned. |
| `q4c_doubt` | credit | no | 0 | The only qualification concerns whether the stacking sentence reaches Annex II products outside Parts A/B (X and Z); nothing flags that the Y answer rests on the absence of a dairy modification document. |
| `q4_cite` | penalty | no | 0 | Penalty not applicable: well cited by clause and page. |
| `q4_fab` | penalty | no | 0 | Penalty not applicable: quotations and page cites match the key's text. |

## Q5: 3.00 / 3

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q5a_p` | credit | yes | 0.525 | no, yes, yes, yes, yes — all five correct. |
| `q5a_q` | credit | yes | 0.525 | yes, no, no, no, no — all five correct. |
| `q5a_r` | credit | yes | 0.525 | yes, yes, yes, no, no, with the correct reason that Part A products are those 'no longer subject' in 11076. |
| `q5a_s` | credit | yes | 0.525 | no, no, no, yes, yes, with the correct reason that Part B products are those 'subject' in 11076. |
| `q5b_dates` | credit | yes | 0.3 | Signed Oct. 23, filed Oct. 29 at 11:15 a.m., published Oct. 30, applies to entries/withdrawals on or after 12:01 a.m. Oct. 30. |
| `q5b_prospective` | credit | yes | 0.15 | 'It does not reach entries made before that time. Neither 11065 nor 11076 contains a refund clause.' |
| `q5c_days` | credit | yes | 0.225 (of 0.225) | P: Sept. 8 to Sept. 15 = 7 days; S: Oct. 23 to Oct. 30 = 7 days. |
| `q5c_silent` | credit | yes | 0.225 (of 0.225) | Notes both scope documents recite the 30-day limit and that 'neither document explains how a 7-day effective date fits that rule', then offers an expressly labelled inference. |
| `q5_cite` | penalty | no | 0 | Penalty not applicable: clause and page citations throughout. |
| `q5_fab` | penalty | no | 0 | Penalty not applicable: no invented sources; recital and clause cites match the key. |

## Q6: 3.00 / 3

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q6a_switzerland` | credit | yes | 0.15 | $8,500; total $12,500. |
| `q6a_norway` | credit | yes | 0.15 | $12,500 flat; total $16,500. |
| `q6a_uk` | credit | yes | 0.15 | $10,000; total $14,000. |
| `q6a_germany` | credit | yes | 0.15 | 10% - 4% = 6% → $6,000; total $10,000. |
| `q6a_taiwan` | credit | yes | 0.15 | $6,000; total $10,000. |
| `q6a_turkiye` | credit | yes | 0.15 | $12,500 flat; total $16,500. |
| `q6a_japan` | credit | yes | 0.15 | 12.5% - 4% = 8.5% → $8,500; total $12,500. |
| `q6a_liechtenstein` | credit | yes | 0.15 | $0 because it is 'not one of the 60 investigated economies'; total $4,000. |
| `q6a_hongkong` | credit | yes | 0.15 | $12,500 flat; total $16,500. |
| `q6a_india` | credit | yes | 0.15 | $10,000 flat; total $14,000. |
| `q6b_germany12` | credit | yes | 0.175 | $0 (MFN 12% at or above the 10% cap). |
| `q6b_japan12` | credit | yes | 0.175 | 12.5% - 12% = 0.5% → $500. |
| `q6b_taiwan10` | credit | yes | 0.175 | $0. |
| `q6b_korea10` | credit | yes | 0.175 | 12.5% - 10% = 2.5% → $2,500. |
| `q6b_swiss_free` | credit | yes | 0.175 | $12,500 (full 12.5%). |
| `q6c_net` | credit | yes | 0.375 | Identifies EU (Germany) and Taiwan moving from 10% flat to 10% net, and Japan and Switzerland from 12.5% flat to 12.5% net, and expressly lists the UK, Norway, Türkiye and Hong Kong as unchanged. |
| `q6c_india` | credit | yes | 0.25 | India 12.5% proposed → 10% adopted, reason given as its adoption of a forced-labor import prohibition after June 5 (memo 47720). |
| `q6_cite` | penalty | no | 0 | Penalty not applicable: determination pages and memo sections cited per economy. |
| `q6_fab` | penalty | no | 0 | Penalty not applicable: no invented source; page cites are consistent with the key's examples. |

## Q7: 1.00 / 1

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q7a_france` | credit | yes | 0.1875 | $60 duty, 0.5% AVE, 9.5% rate, $1,140. |
| `q7b_italy` | credit | yes | 0.125 | $1,800 duty payable, 9% AVE, 1% → $200. |
| `q7b_japan` | credit | yes | 0.125 | 3.5% → $700. |
| `q7b_brazil` | credit | yes | 0.125 | Flat 12.5% → $2,500; no conversion and no cap. |
| `q7c_taiwan` | credit | yes | 0.125 | AVE 11% ≥ 10% cap → $0. |
| `q7c_switzerland` | credit | yes | 0.125 | 1.5% → $300. |
| `q7d_note` | credit | yes | 0.0938 (of 0.09375) | Identifies U.S. note 52(k) (91 FR 47394) and the duty-payable-over-customs-value rule. |
| `q7d_zero` | credit | yes | 0.0938 (of 0.09375) | Locates the zero result in memo section 1(a)(ii) (47720) and the notice's EU/Japan determinations, and correctly says the chapter 99 'less than' language states only the below-cap case; the zero rule is not attributed to note 52(k). |
| `q7_cite` | penalty | no | 0 | Penalty not applicable: adequate citation. |
| `q7_fab` | penalty | no | 0 | Penalty not applicable: no invented source. |

## Q8: 2.00 / 2

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q8a_case1` | credit | yes | 0.1875 | $10,000; the July 29 entry is not before July 28. |
| `q8a_case2` | credit | yes | 0.1875 | $0; loaded July 22, in transit, entered July 27. |
| `q8a_case3` | credit | yes | 0.1875 | $10,000; entry at 12:01 a.m. July 28 is not 'before'. |
| `q8a_case4` | credit | yes | 0.125 | $10,000; loaded 6:00 a.m. July 24, not before 12:01 a.m. |
| `q8a_case5` | credit | yes | 0.125 | $0; entered July 23, before the effective time. |
| `q8a_case6` | credit | yes | 0.1875 | $10,000; withdrawal July 26 is covered and the in-transit exception does not reach warehouse goods. |
| `q8a_case7` | credit | yes | 0.25 | $10,000 on the literal text ('loaded onto a vessel' does not cover air), with the air-freight gap flagged in the uncertainty field. |
| `q8b_where` | credit | yes | 0.25 | 'The in-transit rule is in the DATES line of the notice, 91 FR 47318.' |
| `q8c_dates` | credit | yes | 0.125 | Memo signed July 23, 2026; duties from 12:01 a.m. July 24, 2026; published July 28, 2026. |
| `q8d_july30` | credit | yes | 0.1875 | $10,000; the 9903.04.60-.66 exemption applies only from 12:01 a.m. July 31. |
| `q8d_aug3` | credit | yes | 0.1875 | $0 under note 52(f)(8) as added by Annex I.B. |
| `q8_cite` | penalty | no | 0 | Penalty not applicable: well cited. |
| `q8_fab` | penalty | no | 0 | Penalty not applicable: no invented source. |

## Q9: 2.72 / 3

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q9a_assembly` | credit | yes | 0.5625 | ($100,000 - $35,000) x 12.5% = $8,125. |
| `q9b_repairs` | credit | yes | 0.375 | $6,000 x 12.5% = $750. |
| `q9c_usmca` | credit | yes | 0.2812 (of 0.28125) | $0 under note 52(h). |
| `q9c_no_claim` | credit | yes | 0.2812 (of 0.28125) | 10% x $50,000 = $5,000. |
| `q9d_car` | credit | yes | 0.375 | $0; note 52(f)(2) covers heading 9903.94.01. |
| `q9e_reading` | credit | yes | 0.2812 (of 0.5625) | Concludes 12.5% x $100,000 = $12,500 applies because note 52(f) lists only specified section 232 headings. |
| `q9e_flag` | gate | no |  | (e) presents the result as settled and only restates that note 52(f) 'lists only specified section 232 headings', with no caveat that the proposal and parts of the notice treat all section 232 goods as exempt. The (f) contrast is not referred to from (e), and the only uncertainty given is about image-only annexes, which the criterion excludes. |
| `q9f_232` | credit | yes | 0.2812 (of 0.28125) | Proposal exempted 'all articles and parts currently subject to section 232 tariffs'; adopted note 52(f) lists only particular headings. |
| `q9f_info` | credit | yes | 0.2812 (of 0.28125) | Proposal listed informational materials and donations; the adopted readable text does not mention them (image annex flagged). |
| `q9_cite` | penalty | no | 0 | Penalty not applicable: cited by note and page. |
| `q9_fab` | penalty | no | 0 | Penalty not applicable: no invented source. |

## Q10: 2.40 / 3

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q10a_338` | credit | yes | 0.225 (of 0.225) | $0; clause (2) of 11048 excludes articles subject to section 232 duties. |
| `q10a_301` | credit | yes | 0.225 (of 0.225) | $0; note 52(f)(1) exempts aluminum articles under heading 9903.82.02. |
| `q10a_total` | credit | yes | 0.15 | $6,000 MFN + $100,000 section 232 = $106,000. |
| `q10b_338` | credit | yes | 0.3 | $100,000 via clause (1) of 11065 from Sept. 15. |
| `q10b_total` | credit | yes | 0.15 | $6,000 + $100,000 + $100,000 + $0 = $206,000. |
| `q10c_338` | credit | yes | 0.3 | $30,000; notes that 11046 contains no USMCA exemption. |
| `q10c_301` | credit | yes | 0.3 | $0 under note 52(g); total $30,000. |
| `q10d_stack` | credit | yes | 0.45 (of 0.45) | $30,000 + $6,000 (10% of $60,000) = $36,000. |
| `q10e_excluded` | credit | yes | 0.3 | Excluded from importation under 11061 clause (1); states 'No entry' rather than admitting the goods on payment of duty. |
| `q10f_ieepa` | credit | no | 0 | Says 'The FR shows no 2026 document ending the Canada IEEPA duties' and that the position 'depends on whether EO 14325 remains in effect, which the FR search could not establish'. Executive Order 14389 (2026-03832, 91 FR 9437), which ended the IEEPA duties, is never cited and neither its number nor its document number appears. |
| `q10f_surcharge` | credit | no | 0 | Gives the correct July 24, 2026 end date and the right analysis, but identifies the instrument only as '91 FR 9339, clause (1)'; neither the proclamation number (11012) nor the FR document number (2026-03824) is given, which the criterion expressly requires. |
| `q10_cite` | penalty | no | 0 | Penalty not applicable: adequately cited. |
| `q10_fab` | penalty | no | 0 | Penalty not applicable: checked the non-key sources in (f) — CBP notice 2025-03901 at 90 FR 11743 (effective 2025-03-07) and 90 FR 21487 are real, and the surcharge's '150 days' and section 232 carve-out appear in Proclamation 11012 (fr_grep 2026-03824). The IEEPA answer is a substantive error, not an invented source. |

## Q11: 4.00 / 25

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q11_valid_1` | credit | yes | 2 | Total valid discrepancies: 2. Item by item: (1) section 232 stacking — COUNTED (key #5: clause (2) of 11046/11047/11048 'shall not apply to articles subject to section 232' at 46641/46655/46665 vs 11064(1)/11065(1)/11076(1) 'in addition to' at 58332/58340/68862). (2) body text of 11046 still printing August 19 vs 11056(1) amending only the Annex II chapeau — COUNTED (key #9). (3) 11056 fixing Aug. 22 unconditionally vs later recitals saying Canada reneged and the suspension 'accordingly' lapsed — NOT COUNTED: a matter on which the operative text is merely silent; the recitals describe what 11056's clauses do. (4) FTZ clause (4) keyed to 'the effective date' — NOT COUNTED: duplicate of item (2), resting on the same unchanged body date. (5) notice heading 'Determination To Remove Certain Products' vs the text's 'consistent with the proposal in the June 5, 2026 FRN' — NOT COUNTED: the two are not contradictory, and the submission itself says the June Annex A is an image and 'cannot be checked'. (6) notice's account of the proposal's section 232 exemption vs the narrower note 52(f), with the other side framed as the notice 'not describing that narrowing as a change' — NOT COUNTED: silence is expressly excluded, and the key #8 statement ('all proposed exemptions kept', 47330/47334) is not the statement the submission sets against note 52(f). Exact total: 2. |
| `q11_valid_2` | credit | yes | 2 | Same total: 2 valid discrepancies (items (1) and (2) above). |
| `q11_valid_3` | credit | no | 0 | Same total: 2 — below 3. |
| `q11_valid_4` | credit | no | 0 | Total 2, below 4. |
| `q11_valid_5` | credit | no | 0 | Total 2, below 5. |
| `q11_valid_6` | credit | no | 0 | Total 2, below 6; the submission lists only six items in all, of which two qualify. |
| `q11_valid_7` | credit | no | 0 | Total 2, below 7. |
| `q11_valid_8` | credit | no | 0 | Total 2, below 8. |
| `q11_valid_10` | credit | no | 0 | Total 2, below 10. |
| `q11_valid_12` | credit | no | 0 | Total 2, below 12. |
| `q11_cite` | penalty | no | 0 | Penalty not applicable: each item is located by document and FR page. |
| `q11_fab` | penalty | no | 0 | Penalty not applicable: the notice passage relied on in item (5) — 'Determination To Remove Certain Products From the Proposed Exemption List' and 'consistent with the proposal in the June 5, 2026 FRN' — does appear at 91 FR 47330 (fr_grep 2026-15181); the inference is weak but nothing is invented. |

## Q12: 1.17 / 4

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q12a` | credit | no | 0 | Cambodia is given $6,000; the correct answer is $0 because Cambodia's particular-article list names aloe, Tasmanian pepper, coconut and centella (subheading 1302.19.91) at 91 FR 47366 (confirmed by fr_grep). The submission wrongly says the exemption 'applies only to Jordan'. Malaysia's $6,000 is right. |
| `q12b_exempt` | credit | no | 0 | Gives Malaysia $10,000 and Taiwan $10,000; note 52(j) names Boswellia for Malaysia (47365) and Taiwan has all four articles (47384), so both are $0. |
| `q12b_dutiable` | credit | yes | 0.5 | Bangladesh $10,000 and Argentina $10,000 — both correct (their lists omit Boswellia, 47383). |
| `q12c_taiwan` | credit | no | 0 | Gives 6% = $6,000; Taiwan's list names argan oil, so the section 301 duty is $0. |
| `q12c_japan` | credit | yes | 0.3333 (of 0.333333) | (12.5% - 4%) x $100,000 = $8,500. |
| `q12c_indonesia` | credit | yes | 0.3333 (of 0.333333) | 10% x $100,000 = $10,000. |
| `q12d` | credit | no | 0 | Charges $5,250 / $5,000 / $6,250; sesame seeds for sowing are item (4) of note 52(c) (heading 9903.05.87, 91 FR 47356), so all three are $0. |
| `q12e` | credit | no | 0 | Cambodia is given $4,000 instead of $0 (its list names psyllium, 47366); Thailand $5,000, El Salvador $4,000 and Italy $3,200 are right, but the criterion requires three right including Cambodia. |
| `q12_cite` | penalty | no | 0 | Penalty not applicable: each answer carries a determination page or note citation. |
| `q12_fab` | penalty | no | 0 | Penalty not applicable: the errors are misreadings of the readable note 52(j) text (which does exist at 47365-47394), not invented sources. |

## Q13: 19.00 / 19

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q13a` | credit | yes | 3.3929 (of 3.39286) | ($200,000 - $60,000) x 25% = $35,000, above the 15% floor; clause (2)(d) of 11032 (91 FR 34087) cited. |
| `q13b` | credit | yes | 1.3571 (of 1.35714) | 25% x $200,000 = $50,000. |
| `q13c` | credit | yes | 2.7143 (of 2.71429) | $50,000 on full value; expressly denies the U.S.-content deduction to a non-USMCA product. |
| `q13d` | credit | yes | 2.7143 (of 2.71429) | (15% - 2.5%) x $200,000 = $25,000 under clause (2)(b). |
| `q13e` | credit | yes | 3.3929 (of 3.39286) | $20,000 + $30,000 = $50,000 U.S. content; ($200,000 - $50,000) x 25% = $37,500, citing Commerce guidance 2026-20938 (91 FR 65162) and its Oct. 14 effective date. |
| `q13f` | credit | yes | 1.3571 (of 1.35714) | Gives $45,000 ($180,000 x 25%) expressly because the guidance applies only to entries on or after Oct. 14, 2026, and contrasts the $37,500 result under the guidance. |
| `q13f_flag` | gate | yes |  | Sets out both $45,000 and $37,500 with the Oct. 14 guidance date as what separates them, and the uncertainty field flags that whether U.S.-smelted aluminum in a Canadian part counts before Oct. 14 is unsettled. |
| `q13g` | credit | yes | 2.7143 (of 2.71429) | $15,000 raised to the 15% floor = $30,000, with the floor quoted from clause (2)(d). |
| `q13h` | credit | yes | 1.3571 (of 1.35714) | Through 11:59 p.m. Dec. 31, 2027, then clause (3) of Proclamation 11021 applies from Jan. 1, 2028. |
| `q13_cite` | penalty | no | 0 | Penalty not applicable: clause and page citations throughout. |
| `q13_fab` | penalty | no | 0 | Penalty not applicable: the proclamation and guidance citations match the key; no invented source. |

## Q14: 8.40 / 10

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q14_1_operative` | credit | yes | 0.8 | 'Incorrect. The memo does not give USTR until September 1. Section 2 directs TRQs "as soon as the Trade Representative determines that it is feasible" ... September 1 appears only in the recital'. |
| `q14_1_notice` | credit | no | 0 | Nothing about the USTR notice, the 'subsequent notice' language, the absence of a published notice, or the 10% interim rate — only the memorandum and its recital are discussed. |
| `q14_2` | credit | yes | 1.2 (of 1.2) | Calls it incorrect and gives the proposed-action figures: 'over 1,600 written comments' and 'over 100 witnesses' (memo 47719; notice 47328) — both verified with fr_grep. |
| `q14_3_jordan` | credit | no | 0 | Correctly says Jordan's 10% rests on an ART commitment, not a ban, but never states that Cambodia, Guatemala, Honduras, India, Sri Lanka and Trinidad and Tobago imposed bans after the June proposal — the criterion's second required element is missing. |
| `q14_3_five` | credit | yes | 0.8 | Cambodia and Guatemala were already at 10% in June, so only Honduras, India, Jordan, Sri Lanka and Trinidad and Tobago moved from 12.5% to 10%. |
| `q14_4` | credit | yes | 0.8 | Incorrect; quotes USTR 'determined not to remove' beef, avocados, paprika and the other listed products (47331). |
| `q14_5` | credit | yes | 1.2 (of 1.2) | Incorrect as to Japan and South Korea, which lack economy-specific lists, unlike the EU, Switzerland and Taiwan. |
| `q14_6` | credit | yes | 0.8 | Partly correct: 471 additional products, but only 'certain sugar and sugar containing products' (47331-32). |
| `q14_7` | credit | yes | 1.2 (of 1.2) | Incorrect: the 12.5% is the section 301 rate, added to MFN for flat-rate economies (determinations, 47322-28). |
| `q14_ok` | credit | yes | 1.6 | Calls 8, 9 and 10 all correct and cites a deciding passage for each (47321; 47722-23; 47330). |
| `q14_false` | penalty | no | 0 | No deduction: it does not call statement 8, 9 or 10 incorrect — all three are said to be correct. |
| `q14_cite` | penalty | no | 0 | Penalty not applicable: each item carries a document and page. |
| `q14_fab` | penalty | no | 0 | Penalty not applicable: the 1,600-comment and 100-witness figures attributed to the memorandum at 47719 and the notice at 47328 were checked and do appear there. |

## Q15: 4.29 / 15

| Criterion | Kind | Verdict | Points | Rationale |
|---|---|---|---|---|
| `q15_1` | credit | no | 0 | Gives $25,000 in both cases for February 10, 2025; Executive Order 14197 had paused the Canada duty until March 4, 2025 and the section 232 aluminum duty did not reach Canada until March 12, so the correct answer is $0. |
| `q15_2` | credit | yes | 1.4286 (of 1.42857) | $25,000 in both cases (IEEPA), with the USMCA exemption not yet in effect on March 6. |
| `q15_3` | credit | yes | 1.0714 (of 1.07143) | Case N $25,000 (IEEPA); case U $0 (USMCA exemption from March 7; section 232 not until March 12). |
| `q15_4n` | credit | no | 0 | Gives $50,000 (IEEPA plus section 232), on the mistaken view that 'no non-stacking rule existed until EO 14289, April 29, 2025'; Executive Order 14289 reaches entries on or after March 4, 2025, so only $25,000 is owed. |
| `q15_4u` | credit | yes | 0.7143 (of 0.714286) | $25,000 section 232 aluminum duty, with no Canada duty because of the USMCA exemption. |
| `q15_jun3` | credit | yes | 1.0714 (of 1.07143) | Case N $25,000 IEEPA only (232 not owed under EO 14289 3(a)(ii)); case U $25,000 section 232 at 25% (the 50% rate and reversal begin June 4). |
| `q15_5` | credit | no | 0 | Gives case N $25,000 (IEEPA) and case U $50,000 for June 10, 2025; the correct answer is $50,000 in both cases, since Proclamation 10947 put the 50% section 232 duty in place of the Canada duty for aluminum from June 4, 2025. |
| `q15_6` | credit | no | 0 | Gives case N $35,000 (the 35% IEEPA rate); the section 232 aluminum duty applies instead, so it is $50,000 in both cases. |
| `q15_7` | credit | no | 0 | Gives case N $35,000; both cases should be $50,000 (section 232 at 50%), with no IEEPA or section 122 surcharge on the article. |
| `q15_8` | credit | no | 0 | Gives case N $35,000 IEEPA rather than $50,000 section 232 on the full customs value under Proclamation 11021. |
| `q15_9` | credit | no | 0 | Gives case N $35,000 IEEPA alongside case U's $50,000; both should be $50,000, with no section 301 duty (the section 301 point is right). |
| `q15_10` | credit | no | 0 | For August 25, 2026 it gives case N $35,000 IEEPA plus $100,000 section 338 = $135,000; both cases should be $50,000, because clause (2) of 11048 excludes articles subject to section 232 from the section 338 duty and no IEEPA duty applies. |
| `q15_sep14` | credit | no | 0 | Gives case N $135,000 and case U $50,000 for September 14, 2026; both should be $50,000, since the stacking sentence of 11065 applies only from September 15. |
| `q15_11` | credit | no | 0 | Gives case N $135,000 and case U $150,000 for September 16 and November 10; both cases should be $100,000 (section 232 50% plus section 338 50%), with no IEEPA layer in either. |
| `q15_cite` | penalty | no | 0 | Penalty not applicable: citations are dense and specific. |
| `q15_fab` | penalty | no | 0 | Penalty not applicable: 2025-03664 (90 FR 11423), 2025-03596 (90 FR 11251, effective 2025-03-12), 2025-03901 (90 FR 11743, effective 2025-03-07) and Proclamation 11045 (2026-14990, 91 FR 46635) were checked and all exist and are correctly described. The errors here are misreadings of real provisions (the direction of Executive Order 14289 and the survival of the Canada IEEPA duties), which the criterion treats as loss of credit rather than fabrication. |
