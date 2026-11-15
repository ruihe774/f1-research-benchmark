# Policy Research Task: The 2026 Reduction in Force Rules for Federal Employees

## Your role

You are a policy researcher in the human resources office of a federal executive agency. HR specialists bring you employee situations and policy questions about reductions in force (RIFs). Your job is to find the governing federal documents, read them carefully, and give answers that a specialist could check line by line.

In 2026 the Office of Personnel Management (OPM) rewrote the reduction in force regulations in 5 CFR part 351 and issued several related rules. This task is about those documents: the main final rule, its proposal and corrections, and the other 2026 rules that change what happens to an employee in a RIF.

**Today's date is November 14, 2026.** Treat the Federal Register as of today as the state of the world.

## Your tools

You have five function tools. All of them search and read the U.S. Federal Register (rules, proposed rules, notices, and presidential documents):

- `fr_search`: search documents by keywords and filters (document type, agency, publication date range, docket, RIN, CFR part, sort order, paging). The agency slug for OPM is `personnel-management-office`.
- `fr_doc`: metadata for one document: dates, citation and page range, docket, RIN, CFR parts affected, corrections.
- `fr_toc`: outline of a document's headings, with line numbers.
- `fr_grep`: regex search inside one document's full text, with context lines and the FR page of each match.
- `fr_text`: read a document's full text by line range.

Documents are identified by their FR document number (e.g. 2024-00366), which `fr_search` returns. Long documents are easiest to navigate with `fr_toc`, then `fr_grep`, then `fr_text`. Regulatory amendments usually appear at the end of a rule, after "List of Subjects". In full text, `[[Page N]]` markers give FR page numbers. Tool output sometimes contains command-line hints such as "continue with --start 1201"; these refer to the tool's parameters (here, `start`).

**The Code of Federal Regulations is not available.** A rule prints only the paragraphs it adds or revises. Paragraphs of 5 CFR that no document in the Federal Register prints are outside this task; if an answer depends on one, say so rather than supplying it from memory.

**Limits.** This conversation has a context budget: a fixed number of tokens for everything you read and write, including tool results. Every tool result ends with a line giving the approximate number of tokens left. When the budget is used up, tool calls are disabled and you are asked for your final answer based on what you have found, so plan your reading against it. There is also a turn limit, which is generous.

You have no other tools: no web browsing, no other databases (eCFR, OPM, MSPB or agency websites are not available). Do not rely on memory for facts about documents published in 2025–2026, and do not rely on memory of the RIF rules as they stood before 2026. If something cannot be established from the Federal Register, say so.

## Ground rules

1. **Cite everything.** For every factual claim, cite the FR document number and, where possible, the CFR paragraph (e.g. "40 CFR 60.5397b(b), as amended by 2024-00366") or the FR page (e.g. "89 FR 17062").
2. **Separate the kinds of authority.** Distinguish (a) final regulatory text, (b) preamble explanation, (c) statements made by commenters, (d) proposed rules that are not yet final, and (e) final rules that are not yet in effect.
3. **Say when the text is silent.** If the documents do not answer a question, say so plainly, give the most defensible reading, and explain the uncertainty. A confident answer that the text does not support is worse than a clearly flagged gap.
4. **Show the arithmetic.** When you compute a score or a date, show the inputs, the rule applied, and the result.
5. **Do not give legal advice.** Write as a research memo for an HR specialist, not as instructions to an employee.

## Answer format

When your research is done, give your final answer in the structured format you are given: one entry per question (Q1, Q2, ...), each with three fields:

- **answer:** the direct answer to each lettered part, in order, labelled (a), (b), ...
- **basis:** the provisions and documents relied on, with citations.
- **uncertainty:** anything the documents leave open (write "None" if nothing).

Markdown is fine inside the fields. Each answer must stand on its own: specialists read them separately, so repeat a point rather than refer to another question's answer.

## Assumptions for every scenario

Unless a scenario says otherwise:

- Employees are in the competitive service, in one competitive area and one competitive level, with full-time work schedules. A "career" employee has completed the initial probationary period.
- The agency issued the specific RIF notices on the date given, and each employee received the notice that same day.
- Every rating listed is a rating of record under a five-level pattern (Levels 1 to 5), was issued to the employee with all reviews and signatures, and is on record. A rating "received" on a date was issued and put on record on that date. The agency uses no cutoff date and has not chosen to give any additional or enhanced performance credit.
- A service computation date (SCD) that the scenario gives is already correct for RIF purposes.
- An employee described as a "preference eligible" meets the statutory definition and is not a retired member of a uniformed service. A scenario says so when a preference eligible has a compensable service-connected disability of 30 percent or more. For a retired member of a uniformed service, the scenario gives the facts of the retirement instead, and whether the employee is a preference eligible is for you to work out.
- Every person named in a scenario is qualified for a position only where the scenario says so.

---

## Questions

### Q1

(a) Identify the 2026 final rule that rewrote the retention rules in 5 CFR part 351. Give its FR document number, citation with page range, publication date, effective date, docket number and RIN.
(b) Give the same identification (document number, citation, publication date) for the proposed rule it finalized.
(c) List every correction to that final rule published through today. For each, give the document number, publication date, effective date, and one line on what it corrects.
(d) Which reductions in force do the amended rules govern, and which stay under the earlier rules? Where is this stated?
(e) List every other final rule published in 2026, through today, that amends 5 CFR part 351 (not counting corrections) with effect on or after the main rule's effective date. For each, give the document number, what it changes in part 351, its effective date, and whether it is in force today.

### Q2

An agency must abolish two of the six positions in a competitive level. It issued RIF notices on September 3, 2026. The six employees:

| Employee | Appointment | Veterans' preference | Ratings of record received in the four years before the notices | SCD |
|---|---|---|---|---|
| Abbott | Career | None | Level 5, Level 4, Level 4 | May 1, 2003 |
| Bianchi | Career | Preference eligible with a compensable service-connected disability of 30 percent; not a retired member | Level 4, Level 2, Level 3 | September 10, 2007 |
| Castillo | Career | Retired from the Army as a lieutenant colonel after 22 years of active service; retired pay based on length of service; no service-connected disability | Level 5, Level 4, Level 4 | August 1, 2012 |
| Dalton | Career | Preference eligible; no disability; not a retired member | Only two: Level 5 and Level 2 | March 19, 2018 |
| Eze | Term appointment of four years made in 2023; has completed the probationary or trial period that applied to it; not a career or career-conditional employee | None | Level 4, Level 4, Level 4 | February 5, 2009 |
| Fontaine | Career | None | Only one: Level 4 | June 15, 2015 |

(a) For each employee, give the performance credit, the veterans' preference points and the total, with the arithmetic and the provision applied.
(b) Give the order of retention from highest to lowest standing, explaining every tie. Which two employees are released?
(c) Under the earlier rules, as the 2026 documents describe them, would Bianchi have stood above or below Abbott? Why?
(d) After receiving a notice, Bianchi asks to see how everyone in the level was scored. What is she entitled to see?

### Q3

Each employee below is a career employee and a retired member of a uniformed service. None has been continuously employed in a covered civilian position since 1964.

- A. Retired from the Army as a lieutenant colonel after 22 years of active service; retired pay based on length of service; no service-connected disability.
- B. Retired from the Navy as a commander after 21 years of active service; retired pay based on length of service; a disabled veteran with a compensable service-connected disability rated at 40 percent.
- C. Retired from the Air Force as a major after 14 years; the retirement is a disability retirement for an injury received in the line of duty as a direct result of armed conflict; compensable service-connected disability rated at 60 percent.
- D. Retired from the Army as a master sergeant after 24 years of active service; retired pay based on length of service; no service-connected disability.
- E. Retired from the Army as a staff sergeant on a medical retirement after 16 years, for a training injury that did not result from armed conflict or an instrumentality of war; compensable service-connected disability rated at 10 percent.

(a) For each, say whether the employee is a preference eligible for RIF purposes, how many points are added to the performance credit, and which veterans' preference subgroup the employee is shown in. Give the deciding paragraph for each.
(b) Employee A was appointed to his civilian position on September 7, 2010 and has no earlier civilian service. Two of his 22 years of active service were in a campaign for which a campaign badge was authorized. What is his SCD for RIF purposes? What would it be for employee C, appointed the same day with no earlier civilian service?
(c) What role do the veterans' preference subgroups play in the order of retention under the amended rules?

### Q4

An agency issued RIF notices on September 3, 2026.

(a) Farah's ratings of record were received on November 18, 2022 (Level 4), November 20, 2023 (Level 4), November 15, 2024 (Level 3), November 14, 2025 (Level 3) and August 10, 2026 (Level 5). What is her performance credit?
(b) Suppose instead that the agency's RIF policy sets a cutoff date 45 days before the notices are issued. What is the cutoff date, and what is Farah's performance credit?
(c) Under the cutoff in (b), a further rating of record for another employee was signed by all reviewers and given to the employee on July 15, 2026, but was not entered in the system used by the office that builds the retention registers until August 15, 2026. Can it be used?
(d) Gina's ratings of record were received on August 15, 2022 (Level 5), November 15, 2024 (Level 4) and November 14, 2025 (Level 3). There is no cutoff date. What is her performance credit?
(e) Hank joined the agency in 2025 from an organization whose ratings the agency does not treat as ratings of record, and he has received no rating of record in the last four years. What performance credit does he get?

### Q5

Lee and Park are career employees with no veterans' preference, in the same competitive level. Lee's last three ratings of record are Level 3, Level 3 and Level 3, and his SCD is March 2, 1998. Park's are Level 5, Level 5 and Level 5, and her SCD is July 8, 2019. One of their two positions is abolished.

(a) Who is released if the agency issued the RIF notices on (i) August 28, 2026, with the RIF effective October 27, 2026; (ii) September 2, 2026; (iii) September 3, 2026? For the earlier rules, use only what Federal Register documents say about them, and show the arithmetic.
(b) In case (iii) the RIF was to take effect on November 2, 2026. On October 20 the agency moves the effective date to November 30 and gives both employees amended notices. On October 15 Lee had received a new rating of record of Level 5. Is retention standing recalculated?
(c) Three things are each fixed by a particular event: which version of the rules applies; the end of the four-year period for ratings; and an employee's tenure subgroup and retention standing. Name the event for each, with the provision or passage.

### Q6

Jordan is a career GS-13 employee whose position is in a one-grade interval progression. His current annual rating of record is Level 2, and he has no veterans' preference. He is released from his competitive level. He is qualified for each of the following positions, which are full-time and in his competitive area unless noted:

1. GS-12, held by Ellis, whose retention standing is lower than Jordan's.
2. GS-11, held by Frank, lower standing.
3. GS-10, held by Gale, lower standing.
4. GS-9, held by Hana, lower standing.
5. GS-12, held by Ito, higher standing than Jordan's.
6. GS-12, part-time, held by Kim, lower standing.
7. GS-12, held by Lund, lower standing, in a different competitive area.

(a) To which of these positions does Jordan have an assignment right, and which one must the agency offer? Explain why each of the others is or is not available.
(b) How does the answer change if Jordan is a preference eligible with a compensable service-connected disability of 30 percent or more?
(c) How does it change if Jordan's current annual rating of record is Level 1?
(d) How does it change if Jordan and all seven position holders are in the excepted service?
(e) An old HR handbook says that an employee rated Level 2 cannot take a position held by someone with a higher rating, and it distinguishes "bumping" from "retreating". What do the 2026 documents say about each?

### Q7

Morgan, a career employee, is separated by reduction in force.

(a) Suppose the agency issued her specific RIF notice on August 31, 2026 and the separation took effect on October 30, 2026. Which body hears her appeal? Give every 2026 document that bears on the answer.
(b) Suppose instead that the notice was issued on October 19, 2026 and the separation takes effect on Friday, December 18, 2026. Which body hears her appeal, how must she file, and what is the last day and time for a timely appeal? Show the counting.
(c) In case (b), what must Morgan prove, and is she entitled to a hearing?
(d) In case (b), Morgan's union wants to challenge the separation through the negotiated grievance procedure in its existing collective bargaining agreement. What does the rule say, and what does its preamble say about existing agreements?
(e) In case (b), can Morgan take the final administrative decision to court?
(f) In case (b), before her appeal deadline Morgan filed a complaint with the Office of Special Counsel alleging that her 2025 rating of record was lowered as a prohibited personnel practice. She did not appeal the RIF. On March 10, 2027 the complaint ends in a final decision correcting the rating, which would have changed her retention standing. Can she still appeal the RIF, and by when?
(g) Which provision decides between (a) and (b)? Cite exactly where it is stated.

### Q8

An agency issued RIF notices on October 19, 2026, with separations effective December 18, 2026. On October 26 it put the affected employees on paid administrative leave for the rest of the notice period without asking for their consent.

(a) What does 5 CFR 351.806 say about an employee's status during the notice period? Give both the version that applies today and any version that has been adopted but is not yet in force, with the document and the date it takes effect.
(b) Under the adopted text and its companion leave provision, is employee consent needed, and is there a limit on how long this leave may last?
(c) What does OPM say allowed administrative leave during a RIF notice period before the adopted text takes effect?
(d) Does being on administrative leave change an employee's retention standing, notice rights or appeal rights?

### Q9

An agency's HR office has written up how it ran a RIF in its Tulsa Field Office. The specific RIF notices were issued, and received, on Tuesday, October 13, 2026, and the RIF takes effect on December 14, 2026. All the employees are in the competitive service and all are rated under one five-level pattern. The write-up lists these steps:

1. The Tulsa Field Office is an organizational unit on the agency's official organizational chart. The agency first designated it as a separate competitive area on August 17, 2026. The agency head's designee approved the designation. Nothing was sent to OPM.
2. Ms. Novak, a career-conditional employee hired in March 2026 and still serving her initial probationary period, was kept in her position, while a career employee in the same competitive level was released.
3. Ms. Ortiz has career tenure. She was promoted to her first supervisory position in June 2026 and is serving a supervisory probationary period. Because she is "on probation", she was left off the retention register for her competitive level and was not ranked.
4. The agency's RIF policy sets a cutoff date 30 days before notices are issued. A rating of record that was signed, issued and put on record on October 2, 2026 was used for Mr. Pruitt, because it raised his score. No other employee's later rating was used.
5. Ms. Quist received only two ratings of record in the four years before the cutoff date, a Level 5 and a Level 4. The missing rating was scored as a presumed Level 3, which gave her 7 + 5 + 3 = 15.
6. To recognize exceptional work, the agency added 2 points to the performance credit of every employee who received a quality step increase in the last four years. It announced this in a written policy before the RIF.
7. Two employees at the bottom of one register had the same performance credit with veterans' points, the same tenure subgroup and the same service computation date. The office director chose which of them to release.
8. In one competitive level, the agency released a competing employee while keeping Mr. Reyes, who is in that level on a temporary promotion that ends in March 2027.
9. Mr. Silva, released from his competitive level, was offered a position at a lower grade without any assessment of his qualifications, because he had held that same position until 2023 and received a Level 4 rating of record in it in 2022.
10. For the other released employees, qualification for assignment was decided from an online self-rating questionnaire that is scored automatically.
11. To finish a project, the agency will keep Ms. Tran, who was reached for release, for 60 days after December 14 under the exception for avoiding undue interruption, and then for a further 60 days under its general temporary exception for other reasons.
12. Each notice told the employee that he or she may appeal the action to the Merit Systems Protection Board within 30 days after it takes effect.

Which steps do not comply with the rules that govern this RIF, and which are in order? For each step, cite the provision or passage that decides it. For each step that does not comply, say what the rules require.

### Q10

Nadia is a career GS-12 employee. She received a RIF separation notice on September 8, 2026.

(a) On September 10, 2026 her HR office looked up the definition of "displaced" in 5 CFR 330.602, which governs the agency Career Transition Assistance Plan (CTAP), as it then stood. What did paragraph (1) of that definition contain on that day, and why?
(b) What changed, on what date, and by which document? What reason did OPM give for acting without notice and comment, and how did it characterize the change?
(c) After the change: under part 351, subpart G, Nadia is offered a full-time position with a lower representative rate than her present full-time position, and she declines. Is she still "displaced" under paragraph (1)(i)? What if the offered position had the same representative rate?

### Q11

Compare the regulatory text of 5 CFR part 351 in the proposed rule with the regulatory text in the final rule (the amendments themselves, not the preambles). List every real difference between the two that you can find. For each, name the paragraph and say what the proposed text said and what the final text says. Do not stop at the changes that the final rule's own summary of its changes from the proposal mentions. Differences that are only punctuation, capitalization or citation format do not count; a change in which section, subpart or part a cross-reference points to is not citation format.

### Q12

The Denver Field Office is one competitive area. Seven employees hold the seven GS-13 positions in one of its competitive levels. The positions are in a one-grade interval progression. The agency must abolish three of the seven positions. It issued specific RIF notices to every affected employee on Monday, October 5, 2026, and each received the notice that day. The RIF takes effect on December 4, 2026. The agency has decided that Quinn will stay in her position.

| Employee | Appointment | Veterans' preference | Ratings of record, with the date each was received | SCD |
|---|---|---|---|---|
| Alvarez | Career | None | Level 5 (November 15, 2023), Level 5 (November 14, 2024), Level 4 (November 13, 2025) | April 4, 2011 |
| Brandt | Career | Preference eligible with a compensable service-connected disability of 30 percent | Level 3 (November 15, 2023), Level 4 (November 14, 2024), Level 2 (November 13, 2025) | January 9, 2014 |
| Chen | Career | None | Level 2 (September 30, 2022), Level 5 (November 14, 2024), Level 4 (November 13, 2025). No rating for 2023, when she was on leave without pay | May 22, 2017 |
| Dube | Career-conditional; completed the initial probationary period in 2025 | Preference eligible; no disability | Level 4 (November 14, 2024), Level 4 (November 13, 2025) | August 3, 2015 |
| Estrada | Career | Preference eligible; no disability | Level 4 (November 15, 2023), Level 3 (November 14, 2024), Level 4 (November 13, 2025), Level 5 (October 20, 2026) | February 6, 2012 |
| Farouk | Career | None | Level 3 (November 14, 2024) and no other. He was away for 14 months of uniformed service and was restored to his position under 5 CFR part 353 on July 13, 2026 | October 1, 2019 |
| Quinn | Career-conditional, appointed March 2, 2026; serving the initial probationary period | None | None | March 2, 2026 |

The competitive area has four other positions, each full-time and each in a competitive level of its own:

| Position | Held by | Appointment | Veterans' preference | Ratings of record (received November 2023, 2024, 2025) |
|---|---|---|---|---|
| GS-12 | Gomez | Career | None | Level 5, Level 4, Level 4 |
| GS-11 | Hill | Career | Preference eligible; no disability | Level 4, Level 3, Level 3 |
| GS-10 | Jones | Career | None | Level 4, Level 4, Level 4 |
| GS-9 | Ikeda | Career | None | Level 3, Level 3, Level 3 |

Each of the seven GS-13 employees is qualified for all four of these positions. Gomez, Hill, Jones and Ikeda are each qualified only for the position they hold.

(a) Build the retention register for the GS-13 level. For each of the seven employees, give the performance credit, the veterans' preference points and the total, with the arithmetic, or say why the employee is not on the register. Give the order of retention.
(b) Which three employees are released from the GS-13 level? Explain each choice.
(c) For each released employee, which position must the agency offer, and why not the others?
(d) If every offer is accepted, who is separated from the agency in this RIF?

### Q13

The preamble of the main final rule does not always match what the same document adopts. Find places where a statement in that preamble about what the rule provides differs from the amendatory instructions or regulatory text printed in the same document: for example a different triggering event, a different period, a different category of employee, or a different paragraph. For each, quote or closely paraphrase both sides, and give the FR page of each. List as many as you can find, each once, and say whether another passage of the preamble states the point correctly. Do not list differences between the proposed rule and the final rule here, and do not list matters on which the regulatory text is merely silent.

### Q14

Turn to OPM's final rule on RIF appeals, its correction, its proposal, and the Merit Systems Protection Board's 2026 rule on RIF appeals. Find places of these three kinds:

(i) a statement in the preamble of OPM's appeals rule about what that rule provides that differs from its regulatory text, as published or as corrected;
(ii) a change from the proposed appeals rule to the final appeals rule that the final rule's summary of its changes from the proposal (near the start of its preamble) does not acknowledge;
(iii) an inconsistency within the Board's rule, or between the Board's rule and OPM's rule, about which RIF appeals the Board will still hear.

For each, quote or closely paraphrase both sides and give the FR page of each. List as many as you can find, each once. Do not list matters on which a text is merely silent, and list only items you have checked against the text: items that are wrong count against the answer.
