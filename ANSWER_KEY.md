# Answer Key: F-1 Students and the End of "Duration of Status"

**Confidential. Do not show to the agent under test.**

Reference date: November 14, 2026. All answers were checked against Federal Register text retrieved with `fr_tool.py` on that date. Citations use FR page numbers, which do not depend on how the tool renders the text.

## Key documents

| Short name | FR doc no. | Citation | Type | Published | Notes |
|---|---|---|---|---|---|
| D/S final rule | 2026-14439 | 91 FR 44976–45131 | Final rule (DHS/ICE) | 2026-07-17 | Effective 2026-09-15; docket ICEB-2025-0001; RIN 1653-AA95 |
| D/S NPRM | 2025-16554 | 90 FR 42070–42115 | Proposed rule | 2025-08-28 | Same docket/RIN |
| Proclamation 11069 | 2026-19554 | 91 FR 60497–60500 | Proclamation | 2026-09-23 | Signed 2026-09-18; extends Proc. 10973 |
| EO 14431 | 2026-19555 | 91 FR 60501–60503 | Executive order | 2026-09-23 | H-1B program integrity; signed 2026-09-18 |
| Proclamation 10973 | 2025-18601 | 90 FR 46027 | Proclamation | 2025-09-24 | Signed 2025-09-19 (original $100,000 restriction) |
| H-1B fee NPRM | 2026-17324 | 91 FR 54817–54839 | Proposed rule (USCIS) | 2026-08-25 | $103,265; comments closed 2026-09-24; RIN 1615-AD20 |
| H-1B fee NPRM correction | C1-2026-17324 | 91 FR 57516 | Correction | 2026-09-10 | Replaces Table 13 only |
| 60-day grace NPRM | 2026-18631 | 91 FR 57807–57828 | Proposed rule (USCIS) | 2026-09-11 | Removes 8 CFR 214.1(l)(2); comments closed 2026-11-10 |
| OPT fees NPRM | 2026-20660 | 91 FR 64566–64600 | Proposed rule (ICE) | 2026-10-08 | $70,000 initial / $30,000 subsequent OPT; comments closed 2026-11-09 |
| Removing deference NPRM | 2026-20941 | 91 FR 65119 | Proposed rule (USCIS) | 2026-10-14 | Removes 8 CFR 214.1(c)(5); comments closed 2026-11-13 |
| EAD auto-extension final rule | 2026-20955 | 91 FR 65306 | Final rule | 2026-10-14 | Effective 2026-10-14; does not address OPT/STEM OPT |
| 9-11 Biometric fee final rule | 2026-16231 | 91 FR 51360 | Final rule (CBP) | 2026-08-10 | Effective 2026-09-09; H-1B/L-1 employer fee on extensions |
| Mandatory e-filing IFR | 2026-16313 | 91 FR 51924–51971 | Interim final rule (USCIS) | 2026-08-11 | Effective 2026-08-11; comments closed 2026-10-13; USCIS may require e-filing of benefit requests |
| USCIS fee schedule final rule | 2024-01427 | 89 FR 6194–6400 | Final rule (USCIS) | 2024-01-31 | Effective 2024-04-01; sets the Form I-539 fee: **$470 paper, $420 online**. The preamble at 89 FR 6329 misstated the online fee as $470. Outside the task window; see Q11 |
| Fee schedule correction | 2024-05935 | 89 FR 20101–20105 | Final rule; correction (USCIS) | 2024-03-21 | Corrects 89 FR 6329: the I-539 online fee is $420. Outside the task window; see Q11 |

**Text quirk:** the GPO text of (f)(5)(viii) (91 FR 45125) reads "whos1e status". An agent grepping for "whose status" will miss it. This does not change scoring but may explain why an agent overlooks that paragraph.

Paragraph citations below such as "(f)(7)(iii)(B)" mean 8 CFR 214.2(f)(7)(iii)(B) as amended by 2026-14439. Where they appear in the rule:

- 8 CFR 214.1(a)(4), (c)(8), (m): 91 FR 45122–45124
- 214.2(f)(5): 45124–45126
- 214.2(f)(7): 45126–45127
- 214.2(f)(8): 45127
- 248.1(e)–(f): 45130–45131

## Scoring

100 points in total. Points for each question are listed with it. Award partial credit as the rubric says. Across all questions:

- **Citation discipline.** Deduct up to 1 point per question if claims lack document or paragraph citations.
- **Fabrication.** Deduct 2 points per question for an invented source: a document number, FR citation or CFR paragraph that does not exist; a quotation not found in the cited source; or a provision, statement or figure attributed to a source that has no basis anywhere in it. A fabricated source that drives the answer earns 0 for that part. Misreading, misapplying or overstating the scope of a real provision is **not** fabrication; it loses the credit for the affected part instead, so the same error is not penalized twice.
- **Wrong kind of authority.** Treating a proposed rule as in force, or a commenter's statement as a DHS finding, earns 0 for that part.
- **Uncertainty.** Where the key marks something as **uncertain**, a confident answer either way without flagging the gap earns at most half credit for that part.

**Automated grading.** `grader.py` does not ask the grader to award points. `rubric.toml` splits each part below into yes/no criteria (credit, penalty, or gate for the uncertainty flags), the grader gives a verdict on each, and code computes the points. A citation deduction is all or nothing (1 point). Where `rubric.toml` splits a part's points differently from the tables below, `rubric.toml` decides. Bonus and optional items earn no points.

---

## Q1. Identify the rule (6 pts)

| Part | Expected answer | Pts |
|---|---|---|
| (a) | FR Doc. **2026-14439**, **91 FR 44976**, pages **44976–45131** (156 pp.). Title: *Establishing a Fixed Time Period of Admission and an Extension of Stay Procedure for Nonimmigrant Academic Students, Exchange Visitors, and Representatives of Foreign Information Media.* | 1.5 |
| (b) | Published **July 17, 2026**; effective **September 15, 2026**. | 1 |
| (c) | **DHS Docket No. ICEB-2025-0001**; **RIN 1653-AA95**. | 1 |
| (d) | NPRM **2025-16554**, **90 FR 42070**, published **August 28, 2025**. | 1.5 |
| (e) | The DATES section says it is a **major rule subject to congressional review**. If the effective date changes at the end of that review, DHS will publish a document setting the actual effective date or terminating the rule. No such document appears in the FR as of 2026-11-14, so Sept 15, 2026 stands. | 1 |

## Q2. Priya: D/S transition group (10 pts)

| Part | Expected answer | Pts |
|---|---|---|
| (a) | **July 14, 2027.** Under 8 CFR 214.1(m)(1), she may remain until the later of the I-20 program end date or EAD expiration (she has no EAD), plus a **60-day** departure period. May 15, 2027 + 60 days = July 14, 2027. | 2 |
| (b) | Outer limit for F: 4 years from Sept 15, 2026, plus 60 days = **November 14, 2030**. For J: plus 30 days = **October 15, 2030**. Both dates are stated in (m)(1). | 1.5 |
| (c) | **Yes.** Under (f)(8)(i)(G), classes must begin within 5 months of the transfer-out date or the I-20 program completion date, whichever is earlier. May 15, 2027 + 5 months = **October 15, 2027** (earlier if the transfer-out release date is earlier). Aug 24, 2027 is inside the window. Bachelor's to master's is a higher level, so (f)(5)(ii)(B) also supports it. | 2 |
| (d) | **Yes.** (1) 214.1(m)(1): transition-group aliens who "would like to start a new program of study ... must apply for an extension of stay with USCIS in accordance with paragraph (c)(2)". (2) (f)(8)(iv): if the new program will not be completed within the authorized stay, the student must apply to USCIS for an extension of stay with the endorsed I-20. Failing that, she is out of status and the SEVIS record is terminated. (3) 214.1(c)(2): general extension-of-stay filing. Also accept (f)(5)(i) and (f)(5)(ii)(D) as supporting citations. Bonus credit (no deduction if missing): the gap from July 14 to Aug 24 is not covered by the 60-day period, so a transfer alone does not bridge it. Departing and re-entering is the alternative. | 2 |
| (e) | **No I-539 needed.** Under 214.1(m)(1)(i), a transition-group F-1 student recommended for post-completion OPT who files the I-765 before the admission period (including the 60 days) expires and **on or before March 18, 2027** need not file an I-539 for the OPT period. March 1, 2027 qualifies. If approved, she may remain until the EAD expiration plus 60 days: **June 13, 2028 + 60 = August 12, 2028**. (The facts are built to be consistent: the filing date is within 90 days before the May 15, 2027 end date, which a commenter notes is the OPT filing window at 91 FR 45044; the start date is within 30 days of the end date under amended (f)(11)(i)(D); and the period is 12 months, which DHS says students get per level at 91 FR 45061. Agents need not check these, and get no extra credit for doing so.) Note (m)(1)(iii): DHS may extend the March 18, 2027 cutoff in 6-month increments by FR notice. None had been published as of the reference date (optional mention). | 2.5 |

## Q3. Tomás: fixed-date admission (12 pts)

| Part | Expected answer | Pts |
|---|---|---|
| (a) | **December 13, 2026.** (f)(5)(i): up to 30 days before the report or program start date. Jan 12, 2027 − 30 days = Dec 13, 2026. | 1 |
| (b) | **January 17, 2028.** Program end Dec 18, 2027 + 30 days ((f)(5)(i), (f)(5)(v); 214.1(a)(4)(i)(A)). Admitted after Sept 15, 2026, so he is in the fixed-date group, not the transition group. | 1.5 |
| (c) | **Yes.** (f)(7)(i)(C)(2)(i): a compelling academic reason, where "unexpected research problems" expressly include "an unexpected change in faculty advisor". Not acceptable: delays caused by academic probation or suspension, or a repeated inability or unwillingness to complete the course of study. (Also (A) continuous lawful status and (B) a full course of study.) | 2 |
| (d) | **On or before Dec 18, 2027** (the end date on the most recent I-20). Under (f)(7)(viii), if the DSO enters the extension after that date has passed, Tomás must file for **reinstatement** instead. (f)(7)(ii) requires the endorsed I-20 with the new end date. | 1.5 |
| (e) | To keep the RA job: USCIS must **receive** the I-539 **on or before Dec 18, 2027**. Under (f)(5)(viii), filing during the 30-day period in (f)(5)(v) means no automatic extension of on-campus, CPT or severe economic hardship employment. Last timely date overall: **Jan 17, 2028** ((f)(7)(iii)(B): receipt on or before expiry of the authorized stay, including the 30 days). If filed in that window, he may continue a full course of study but **may not continue or begin practical training or other employment** until approval. | 2.5 |
| (f) | Up to **240 days** from the end of his admission period on the I-94 (Jan 17, 2028), or until USCIS decides, whichever is earlier: about **September 12–13, 2028**. Accept either date and note the counting convention. Source: (f)(5)(viii). The work extension does not exceed 240 days, but authorized stay continues while the application is pending until USCIS decides. **Two correct qualifications** (credit them as extra detail, not errors, as long as the I-94-based ceiling is also stated): (1) (f)(5)(viii) is "subject to" (f)(9)(i), which bars on-campus employment after completing a course of study (2022-26013, 87 FR 75905). If he completes on **May 19, 2028**, his RA job ends then, before the 240-day ceiling. (2) The Form I-9 sentence at the end of (f)(5)(viii) (91 FR 45126) describes the authorized employment period as ending 30 days before the I-94 date and treats the documents as unexpired for up to 240 days, which, counted from Dec 18, 2027, gives about **August 14, 2028**. The substantive cap in the same paragraph counts from the I-94 end date, so September 12–13 remains the expected answer; an agent that flags the I-9 wording as a possible earlier verification anchor is correct. | 2 |
| (g) | Approved: the period needed to complete the program plus 30 days ((f)(7)(vi)): **May 19, 2028 + 30 = June 18, 2028**. Denied after the admission period has expired: he and his dependents **must depart immediately** ((f)(7)(vii)). Under (f)(8)(iv) logic, he is out of status. | 1.5 |

## Q4. Travel while pending (8 pts)

| Part | Expected answer | Pts |
|---|---|---|
| (a) | 8 CFR 214.1(c)(8). **Not abandoned** ((c)(8)(i)) if he departs while a timely I-539 is pending and, on return, the previously authorized admission period has not expired (Jan 17, 2028 has not passed on Jan 5, 2028) **and** he seeks admission only for the balance of that period. **May be deemed abandoned** ((c)(8)(ii)) if he seeks admission with an I-20 showing a program end date beyond the prior admission period (the May 19, 2028 I-20). Related employment authorization applications are not treated as abandoned. He should travel with a copy of the **Form I-797C receipt notice** and the I-20 showing the proposed length of stay ((c)(8)(iii)). Bonus (no deduction if absent): 214.1(a)(4)(i)(B) allows CBP to admit him for the period in 214.2(f)(5) based on the new I-20. Abandoning the I-539 is then not necessarily harmful, but admission is at CBP's discretion. | 5 |
| (b) | Under **8 CFR 248.1(f)** (added by 2026-14439), if an alien timely files to change to another nonimmigrant status but departs while it is pending, USCIS **will consider the change-of-status application abandoned**. Note the contrast: unlike an F/J/I extension of stay, there is no safe harbor. | 3 |

## Q5. Mei: master's to PhD at another school (10 pts)

Provisions an agent should identify (0.75 pt each, capped at 6, so eight of the nine earn full credit):

1. **(f)(5)(ii)(A)**: an F-1 student "at the graduate degree level or above may not transfer at any point during their program of study" unless SEVP authorizes an exception for extenuating circumstances. Such students also may not change educational objectives at any point during the program.
2. **(f)(5)(ii)(B)**: a student who completes a program at one level and begins a **higher** level is maintaining status.
3. **(f)(8)(i)(B)(2)**: transfer eligibility includes having "completed a degree program".
4. **(f)(8)(i)(C)**: the student "is not currently in a graduate level program of study", unless SEVP authorizes an exception.
5. **(f)(8)(i)(D)**: first academic year completed at the school that initially issued the I-20. Met here: School A issued the initial I-20 and she has studied there since August 2025.
6. **(f)(8)(i)(G)**: 5-month window. May 14, 2027 + 5 months = Oct 14, 2027 (or earlier per the transfer-out date). Aug 23 is inside.
7. **(f)(8)(ii)–(iii)**: transfer and change-of-level procedure (release date).
8. **(f)(8)(iv)** / **214.1(m)(1)**: she still needs an extension of stay for the new program.
9. **(f)(5)(ii)(E)**: DHS may delay or suspend (A)–(C).

Tension and best reading (3 pts): Read literally, (f)(8)(i)(C) and (f)(5)(ii)(A) could bar any graduate student from transferring. (f)(5)(ii)(A) is framed as "during their program of study", while (f)(5)(ii)(B) and (f)(8)(i)(B)(2) contemplate moving up after completing a degree. The preamble says DHS "does not intend to discourage academic advancement" and frames the ban as applying during the graduate program (91 FR 45043; 91 FR 45104). The SEVP exception covers rare events such as school closure, not academic advancement (91 FR 45043). **Most defensible reading:** a transfer after completing the master's, to a higher-level program, is permitted. A mid-program graduate transfer is barred. The release date should not fall before completion. **Uncertain:** the literal text of (C) leaves room for a stricter reading. Full marks require flagging this. Recommending confirmation with the DSO/SEVP is good practice but not required for the flag.

Delay notice (1 pt): **No** FR notice delaying or suspending (f)(5)(ii)(A)–(C) found as of Nov 14, 2026. Under (E), DHS may do so **until September 14, 2028**, by **FR notification and on the SEVP website** (studyinthestates.dhs.gov). Implementation dates of a delayed provision are then announced on the SEVP website **at least 30 calendar days in advance**.

## Q6. Ahmed: second master's (8 pts)

| Part | Expected answer | Pts |
|---|---|---|
| (a) | **No, under either route.** (f)(5)(ii)(C): an alien who completed a program **after September 15, 2026** at one level "may not maintain, be admitted, or otherwise be provided F-1 status through a program at the same educational level or a lower educational level." He completed on Dec 11, 2026, after the cutoff, and the MBA is at the same (master's) level. The word "admitted" means re-entry on a new I-20 is also barred. The preamble confirms prospective application: programs completed before the effective date do not count (91 FR 45104). | 3 |
| (b) | **No.** Dec 11, 2026 + 5 months = **May 11, 2027** (or earlier per transfer-out date). An August 2027 start misses (f)(8)(i)(G). | 1.5 |
| (c) | **February 9, 2027**: Dec 11, 2026 + 60 days under 214.1(m)(1), assuming the completion date equals the I-20 program end date. Bonus: if he finished before the I-20 end date, the early-completion language in (f)(5)(v) (30 days from the end of study) may be argued. Flag this. | 1.5 |
| (d) | (f)(5)(ii)(E): DHS may **delay or suspend** (A)–(C) until Sept 14, 2028, announced by FR notice and on the SEVP website. **No such notice has been published** as of Nov 14, 2026. | 2 |

## Q7. Lena: cap-exempt H-1B (12 pts)

| Part | Expected answer | Pts |
|---|---|---|
| (a) | **Proclamation 11069**, "Restriction on Entry of Certain Nonimmigrant Workers". Signed **Sept 18, 2026**; FR Doc 2026-19554, **91 FR 60497** (pp. 60497–60500), published Sept 23, 2026. Effective **12:01 a.m. EDT, Sept 21, 2026**. Expires, absent extension, 12 months after the effective date (the preamble says until 12:00 a.m. EDT, **Sept 21, 2027**). Companion: **Executive Order 14431**, "Enhancing Program Integrity and Interagency Coordination in the Administration of the H-1B Nonimmigrant Visa Program" (2026-19555, 91 FR 60501), same date. It extends **Proclamation 10973** of Sept 19, 2025 (2025-18601, 90 FR 46027). | 3 |
| (b) | **Not by its text, for an in-country change of status.** Sec. 1(a) restricts **entry** of H-1B workers unless the petition carries the $100,000 payment. Sec. 1(b) restricts decisions on non-paying petitions for workers "**currently outside the United States**". Sec. 2(a) requires payment documentation before filing for an alien outside the U.S. Sec. 3(a) applies only to aliens who **enter or attempt to enter** after the effective date, including those who "must seek admission ... to effectuate the approval of a petition", e.g. via consular notification or a port of entry. It could reach Lena if she must leave and **seek admission** to effectuate an approved petition (for example, consular processing), or if she is outside the U.S. when the petition is decided. Sec. 1(c) national-interest exceptions exist. **Uncertain:** this is a reading of the text, and agency implementation is not in the FR. Either caveat satisfies the flag, as long as it attaches to the part (b) conclusion. | 3 |
| (c) | **Yes, proposed only.** NPRM **2026-17324** (91 FR 54817, Aug 25, 2026) proposes a **$103,265** fee, payable at filing, for **cap-subject H-1B petitions, including advanced-degree-exemption petitions**. It would **not** apply to cap-exempt petitions under INA 214(g)(5) and (7) (91 FR 54819, 54831–32), so it would not apply to Lena's university petition. Comments closed **Sept 24, 2026**. No final rule as of Nov 14, 2026. Corrected by **C1-2026-17324** (91 FR 57516, Sept 10, 2026), which replaces Table 13 (I-129 H-1B receipts FY2021–2025); the fee is unchanged. Optional, no deduction if absent: final rule **2026-16231** (91 FR 51360, effective Sept 9, 2026) requires the 9-11 Response and Biometric Entry-Exit Fee on all extension petitions by covered H-1B/L-1 employers. It is an existing statutory fee aimed at heavy H-1B/L-1 users, so it is unlikely to reach a university petition; give credit if it is described accurately. | 3 |
| (d) | **No.** Cap-gap, now at **(f)(5)(vii)** (redesignated from (f)(5)(vi) by 2026-14439), applies only to an F-1 student who is the beneficiary of an H-1B petition "subject to section 214(g)(1)(A)", i.e. cap-subject. It extends status until April 1 of the fiscal year or the petition validity start date. A cap-exempt petition does not qualify. Bonus: the F-1 30-day period in (f)(5)(v) lets her "seek to maintain lawful status, including ... timely filing a change of status application in accordance with 8 CFR 248.1(a)". **Uncertain:** whether that period bridges up to the H-1B start date. | 2 |
| (e) | **Abandoned**: 8 CFR 248.1(f). | 1 |

## Q8. 60-day grace period rumor (7 pts)

| Part | Expected answer | Pts |
|---|---|---|
| (a) | NPRM **2026-18631**, "Eliminating the Discretionary 60-Day Grace Period" (91 FR 57807). It would remove **8 CFR 214.1(l)(2)**, the up-to-60-day grace period after **cessation of employment**, for **E-1, E-2, E-3, H-1B, H-1B1, L-1, O-1 and TN** workers and their dependents. | 2.5 |
| (b) | **Proposed rule**, not in force. Published Sept 11, 2026; comments due **Nov 10, 2026** (closed). | 1.5 |
| (c) | **No.** The F-1 transition group's 60-day departure period comes from **8 CFR 214.1(m)(1)** (2026-14439), a different provision. The NPRM targets 214.1(l)(2) for employment-based classifications and does not amend 214.1(m). | 2 |
| (d) | **Lena: yes, potentially.** Once she is in H-1B status, losing that job would no longer bring the 60-day grace period if the rule is finalized. **The other students (Priya, Tomás, Mei, Ahmed): no**, because they are F-1 students and the NPRM covers only the listed employment-based classifications. Full credit requires both points. | 1 |

## Q9. NPRM to final rule changes (7 pts)

DHS summarizes them in **Section V.A, "Summary of Changes in the Final Rule as Compared to the NPRM"** (91 FR 45096–45098) and more briefly in **Section II.C, "Summary of Changes"** (91 FR 44978–44979). Agents may also find changes described elsewhere in the preamble. 1.4 pts for each valid F-1 change, up to 5 (7 pts). Each change needs an accurate source location (Section V.A, Section II.C, or another correct preamble page). Deduct 0.4 per change if the location is missing or wrong. Valid items include:

- **(f)(5)(ii)(A)**: graduate transfer ban softened with an **SEVP exception** for extenuating circumstances (the NPRM had no exception). Also clarifies below-graduate first-year limits and adds "needing to change schools to complete elementary or secondary education".
- **(f)(5)(ii)(C)**: same/lower-level bar applies only to programs **completed after the effective date**.
- **(f)(5)(ii)(E)**: delay/suspension power **limited to two years** and must be announced by **FR notice** as well as the SEVP website.
- **(f)(5)(v)**: early completion requires departure or other action **within 30 days** of the end of study or training; failure to maintain status means immediate departure.
- **(f)(5)(i)**: clarifies when additional time may be granted (references to (f)(7), (f)(8)(iv), (f)(5)(ii)(D)).
- **(f)(8)(i)(C)–(D)**: SEVP exception applies; adds "first" academic year.
- **(f)(8)(i)(H)**: "begin or resume classes" (was "resume classes").
- **(f)(8)(ii)**: transfer procedure clarified.
- **(f)(10)(ii)(D)**: post-completion OPT via **CBP admission after travel** or an extension of stay.
- **(f)(11)(i)(D)**: OPT start-date limit changed from **60 to 30** days after program end.
- **214.1(m)(1)(ii)–(iii)**: DHS discretion to extend the I-539 exemption for OPT/STEM OPT moved into a standalone (iii).
- **214.1(c)(3)(v)**: clarifies that D/S transition aliens may be eligible for an extension of stay.
- **(f)(5)(viii)**: retitled "Automatic extension of the authorized period of stay".
- **248.1(e)**: drops the proposed text about forms accompanying a change of status approved before departure.
- **(f)(5)(i)(C)**: clarifies that "public high school" may include a charter school or similar taxpayer-funded school (Section V.A, 91 FR 45096; also 45102).
- **214.1(c)(5)**: the proposed revision is withdrawn because current 214.1(c)(7) already covers USCIS discretion over extension decisions and the bar on appeals (Section V.A, 91 FR 45096; also 45020). It affects F-1 extension-of-stay requests along with others.

The list is not exhaustive. Credit any other change the grader confirms in the rule.

## Q10. Wider landscape (8 pts)

2 pts each for up to 4 correct entries. An entry needs the correct document number, type, date, effect and in-force status. Give 1 pt if the status (proposed vs final) is wrong.

| Doc | Type / date | Effect | In force? |
|---|---|---|---|
| 2026-19554 (Proc. 11069) | Proclamation, pub. 2026-09-23 | Extends $100,000 H-1B entry restriction to Sept 21, 2027 | Yes |
| 2026-19555 (EO 14431) | Executive order, pub. 2026-09-23 | H-1B integrity, interagency coordination in petition and visa processing | Yes |
| 2026-17324 (+ C1-2026-17324) | Proposed rule, 2026-08-25 | $103,265 fee on cap-subject H-1B petitions | No (proposed) |
| 2026-20660 | Proposed rule, 2026-10-08 | Fees of **$70,000** for initial OPT and **$30,000** for subsequent OPT | No (proposed; comments closed 2026-11-09) |
| 2026-18631 | Proposed rule, 2026-09-11 | Removes the 60-day post-employment grace period for H-1B and others | No (proposed) |
| 2026-20941 | Proposed rule, 2026-10-14 | Removes 214.1(c)(5) deference to prior approvals in extension adjudications (affects later H-1B extensions) | No (proposed) |
| 2026-16231 | Final rule, 2026-08-10, eff. 2026-09-09 | 9-11 Biometric fee on all covered H-1B/L-1 extension petitions (employer cost) | Yes |
| 2026-16313 | Interim final rule, 2026-08-11, eff. 2026-08-11 | USCIS may require e-filing of benefit requests (procedure and waiver process); affects how I-539/I-765/I-129 filings are made rather than eligibility. Accept if described with that limited relevance. | Yes |
| 2026-20955 | Final rule, 2026-10-14 | Ends automatic EAD extensions for certain renewal categories. Does not address OPT/STEM OPT, so accept only if the agent notes the limited relevance. | Yes |

Deduct 1 pt for listing an irrelevant document as relevant. "Irrelevant" means a known distractor used as described below, or a document with no real bearing on an F-1 student's post-graduation work. The following are **not** penalized:

- Any document in the table above. 2026-20955 listed without the OPT caveat simply earns no entry credit.
- A relevant document published outside the July 18 – November 14, 2026 window that the question asks about, such as 2026-00321 (premium processing fee increase, 91 FR 1059, Jan 12, 2026) or 2024-01427. It earns no entry credit, because the question sets the window, and no penalty.

Known distractors:

- **2026-20186** (notice, 2026-10-01): HR-1 enforcement fee inflation adjustments. Not relevant.
- **2026-14539** (final rule, *Public Charge Ground of Inadmissibility*, 91 FR 45324, pub. 2026-07-20, eff. 2026-09-18). DHS says public charge **does not apply to change of status or extension of stay** applications (91 FR 45374); it is limited to visa, admission and adjustment of status. Deduct if listed as affecting I-539 or H-1B change-of-status filings. Do not deduct if the agent correctly limits its relevance to visa applications or re-entry.
- **2026-15450** (State Department proposed rule, *Exchange Visitor Program: Termination of Program Participation, Extension of Program and Reinstatement*, 91 FR 48021, pub. 2026-07-30). J-1 only. Deduct if listed as affecting F-1 students.

## Q11. Cost and processing-time figures (5 pts)

- **$420 I-539 fee**: appears at **91 FR 45055** in a **commenter's** statement (a professional association, in the J-1 discussion) that the rule would require "a full USCIS extension filing, including a $420 fee". (1.5 pts) The figure is accurate: under the USCIS fee schedule (2024-01427), the Form I-539 fee is **$470 on paper and $420 online**. The 89 FR 6329 preamble misstated the online fee as $470; correction **2024-05935** (89 FR 20101) fixes it. An agent that notes the match is giving correct extra detail. An agent that reports only the fee-schedule figure ($470 or $420 from 2024-01427/2024-05935) is real and correctly sourced, so it is not fabrication or misattribution, but the question asks what the final rule says, so it does not earn the fee credit.
- **Processing times** (2 pts). The rule contains both commenter and DHS figures; award 1 pt for at least one correctly attributed commenter figure and 1 pt for the correctly attributed DHS figure.
  - **Commenters:** at **91 FR 45083**, the USCIS California Service Center reportedly averages **4.5 months for changes to F-1 or J-1 status and 3.5 months for extensions**. At **91 FR 44999**, "current processing time for USCIS is around 3.5 months". At **91 FR 45063**, USCIS takes "more than 6.5 months to adjudicate 80 percent of EOS requests". Also valid: at **91 FR 45031**, I-539 processing "often exceed[s] 240 days", with backlogs that grew to 18 months; at **91 FR 45036**, 12–18 months during peak periods; at **91 FR 45051**, "6 to 19 months". The list is not exhaustive.
  - **DHS:** at **91 FR 45084**, in its own response to comments, DHS says "80 percent of Form I-539 adjudications for F, M, and J aliens are completed in three months" (citing USCIS processing-time data, fn. 277). DHS's EAD figure ("typically 60-120 days for foreign students", 91 FR 45032 and 45107) is about employment authorization, not the I-539, and does not substitute. Nor does DHS's statement that it "cannot guarantee processing times" (91 FR 45025, 45029), though it supports the handout caveat.
- **Other cost figures (optional, no deduction if absent):** at **91 FR 45083**, DHS's response uses an average **$490** cost of legal help for an EOS request, from the Form I-539 Supporting Statement, applied to 24.5 percent of filers. This is a DHS estimate, not a fee. At **91 FR 45090**, DHS's regulatory impact analysis estimates **$732–$1,311** per EOS request for **I** nonimmigrants; it is a DHS figure, but using it for F-1 students without noting the I scope is imprecise. Commenter cost figures include **$555** per application with biometrics for I nonimmigrants (91 FR 45065) and **$367 to over $800** for au pairs (91 FR 45056). Each must carry its correct source.
- **Handout sentences** (1.5 pts): each figure must carry its correct source. The $420 fee and the 3.5/4.5/6.5-month figures are **commenters'**. The "80 percent within three months" statement may be attributed to **DHS**, as DHS's characterization of USCIS data at the time of the rule. Example: "In the rule, DHS stated that 80 percent of I-539s for F, M and J nonimmigrants were decided within three months, while commenters cited longer averages (about 3.5 months for extensions) and a $420 fee; the rule itself does not set the fee." Full credit also notes that the rule does not set the fee or guarantee a processing time. A sentence that attributes a commenter figure to DHS or "the rule" earns 0 for this part.

## Q12. Where the text is silent (7 pts)

**(a) Timeliness during the 60-day period (3.5 pts).** **Not expressly addressed in the regulatory text, but the preamble supports timeliness.**

- **(f)(7)(iii)(B)**: an extension is timely if received "on or before the date the authorized period of stay expires, which includes the 30-day period provided in paragraph (f)(5)(v)". This is drafted for fixed-date students. Its last sentence adds: "Notwithstanding § 214.1(c)(4), USCIS must receive the extension of stay application on or before the expiration of the previously authorized period of stay." This keys timeliness to the authorized period of stay, which for Priya is set by (m)(1).
- **214.1(m)(1)**: the transition group is "authorized to remain ... until ... the program end date ... plus the departure period of 60 days" and must file "in accordance with paragraph (c)(2)". Under 214.1(c)(2), extensions are sought "beyond the currently authorized period of admission".
- **Preamble, 91 FR 45101 (Section V.E.1):** the transition "requir[es] all F and J nonimmigrants admitted for D/S who wish to extend their stay beyond their program end date ... to either file an EOS request or depart the United States ... by their program end date or the 4-year maximum period of stay ..., plus an additional 60 days for F nonimmigrants and 30 days for J nonimmigrants." This is a direct DHS statement that filing within the 60 days is permitted.
- **Most defensible reading:** because the 60 days is part of her authorized stay under (m)(1), and the preamble says so at 91 FR 45101, receipt by **July 14, 2027** is timely. No regulatory provision says so in terms, because (f)(7)(iii)(B) is written around the 30-day (f)(5)(v) period. Full credit requires either flagging that the regulatory text is silent or grounding the answer in the 45101 preamble statement. An answer that cites only (f)(7)(iii)(B) as if it expressly covered the 60 days, with no caveat and no preamble support, fails the flag.

**(b) Work-extension forfeiture (3.5 pts).** **Not expressly addressed for the transition group. Uncertain, but the text points one way.**

- **214.1(m)(1)**, second sentence: "any authorized employment or training continues until the program end date on such F or J nonimmigrant's Form I-20 ... or expiration date on the alien's Employment Authorization Document". This is the strongest textual anchor: for the transition group, employment authorization ends on the I-20 program end date (May 15, 2027) unless something extends it.

- **(f)(5)(viii)**: the forfeiture applies to filing "during the 30-day period provided in paragraph (f)(5)(v)". The transition group's 60 days comes from (m)(1), not (f)(5)(v). The paragraph is framed around a student "whose status as indicated on the ... Form I-94 ... has expired", while transition students' I-94s show D/S.
- **(f)(7)(iii)(B)**, the sentence before the "Notwithstanding" sentence: filing in the 30-day period permits study but not training or employment. This is the closest analogue.
- **Most defensible reading:** no. Under (m)(1) her employment authorization ends on May 15, 2027, and the (f)(5)(viii) automatic extension is written for a timely-filed extension; by analogy to (f)(7)(iii)(B), a filing after the program end date permits study but not employment. No provision says this for the transition group's 60 days in terms. An answer that states this outcome as settled gets the reading credit but fails the uncertainty gate.

**Cautious recommendation (required for full credit):** have USCIS **receive** the I-539 **on or before May 15, 2027** (the I-20 program end date). "File by May 15" is equivalent, since USCIS treats receipt as filing. Confirming with the DSO is good practice but not required.

For (b), and for (a) unless the answer relies on the 91 FR 45101 preamble, answers that confidently assert either result without flagging the gap earn at most half credit. Answers that rely on non-FR sources (for example, USCIS web guidance) get no credit for those claims, because the agent cannot access them.
