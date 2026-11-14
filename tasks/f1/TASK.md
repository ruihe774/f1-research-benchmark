# Policy Research Task: F-1 Students and the End of "Duration of Status"

## Your role

You are a policy researcher supporting the international student office of a U.S. university. Advisers bring you student situations and policy questions. Your job is to find the governing federal documents, read them carefully, and give answers that an adviser could check line by line.

**Today's date is November 14, 2026.** Treat the Federal Register as of today as the state of the world.

## Your tools

You have five function tools. All of them search and read the U.S. Federal Register (rules, proposed rules, notices, and presidential documents):

- `fr_search`: search documents by keywords and filters (document type, agency, publication date range, docket, RIN, CFR part, sort order, paging).
- `fr_doc`: metadata for one document: dates, citation and page range, docket, RIN, CFR parts affected, corrections.
- `fr_toc`: outline of a document's headings, with line numbers.
- `fr_grep`: regex search inside one document's full text, with context lines and the FR page of each match.
- `fr_text`: read a document's full text by line range.

Documents are identified by their FR document number (e.g. 2024-00366), which `fr_search` returns. Long documents are easiest to navigate with `fr_toc`, then `fr_grep`, then `fr_text`. Regulatory amendments usually appear at the end of a rule, after "List of Subjects". In full text, `[[Page N]]` markers give FR page numbers. Tool output sometimes contains command-line hints such as "continue with --start 1201"; these refer to the tool's parameters (here, `start`).

**Limits.** This conversation has a context budget: a fixed number of tokens for everything you read and write, including tool results. Every tool result ends with a line giving the approximate number of tokens left. When the budget is used up, tool calls are disabled and you are asked for your final answer based on what you have found, so plan your reading against it. There is also a turn limit, which is generous.

You have no other tools: no web browsing, no other databases (eCFR, USCIS, SEVP or agency websites are not available). Do not rely on memory for facts about documents published in 2025–2026. If something cannot be established from the Federal Register, say so.

## Ground rules

1. **Cite everything.** For every factual claim, cite the FR document number and, where possible, the CFR paragraph (e.g. "40 CFR 60.5397b(b), as amended by 2024-00366") or the FR page (e.g. "89 FR 17062").
2. **Separate the kinds of authority.** Distinguish (a) final regulatory text, (b) preamble explanation, (c) statements made by commenters, (d) proposed rules that are not yet final, and (e) presidential documents.
3. **Say when the text is silent.** If the documents do not answer a question, say so plainly, give the most defensible reading, and explain the uncertainty. A confident answer that the text does not support is worse than a clearly flagged gap.
4. **Show date arithmetic.** When you compute a date, show the start date, the period added, and the result.
5. **Do not give legal advice.** Write as a research memo for an adviser, not as instructions to a student.

## Answer format

When your research is done, give your final answer in the structured format you are given: one entry per question (Q1, Q2, ...), each with three fields:

- **answer:** the direct answer to each lettered part, in order, labelled (a), (b), ...
- **basis:** the provisions and documents relied on, with citations.
- **uncertainty:** anything the documents leave open (write "None" if nothing).

Markdown is fine inside the fields. Each answer must stand on its own: advisers read them separately, so repeat a point rather than refer to another question's answer.

Unless a question says otherwise, assume each student has always maintained status, never worked without authorization, is not on probation, and that the I-20 report date equals the program start date.

---

## Questions

### Q1

DHS recently ended "duration of status" admission for F-1 students. Identify the final rule that did this and give: (a) its FR document number and citation, including page range; (b) publication date and effective date; (c) docket number and RIN; (d) the proposed rule it finalized (document number, citation, publication date); and (e) whether anything has changed, or could still change, its effective date.

### Q2

Priya was admitted as an F-1 student for "D/S" in August 2023 and was maintaining status on September 15, 2026. Her I-20 shows a bachelor's program end date of May 15, 2027. She has no EAD.

(a) Under the rule, until what date is Priya authorized to remain in the U.S. without filing anything? Name the provision and show the arithmetic.
(b) What is the latest date on which anyone admitted for D/S and in status on September 15, 2026 could still be authorized to remain under this arrangement? Answer separately for F and J nonimmigrants.
(c) Priya will start a master's program at a different university on August 24, 2027. Can her SEVIS record be transferred for that program, as far as timing is concerned? State any deadline that applies.
(d) Does she need to file anything with USCIS for the new program? Cite every provision that supports your answer.
(e) Alternative facts: instead of going straight to the master's, Priya is recommended for post-completion OPT and files her Form I-765 on March 1, 2027, requesting OPT from June 14, 2027 through June 13, 2028. What must she file to remain in the U.S. for the OPT period? If the OPT is approved as requested, until what date may she remain?

### Q3

Tomás has an I-20 for a master's program running January 12, 2027 to December 18, 2027. He enters the U.S. in F-1 status on December 20, 2026, and holds an on-campus research assistant job. In October 2027 his faculty advisor leaves the university, and his DSO issues an I-20 with a new program end date of May 19, 2028.

(a) What is the earliest date on which Tomás could have been admitted for this program?
(b) What admit-until date should his I-94 show?
(c) Can the advisor's departure support a request for more time? Name the provision. Name one reason the rule says would not.
(d) Is there a deadline for the DSO to enter the new program end date in SEVIS? What follows if it is missed?
(e) Tomás wants his RA job to continue without interruption while USCIS considers his request. By when must USCIS receive his application? Would a later filing still be timely, and if so, with what consequences?
(f) If he files in time to keep working, how long can the RA job continue while the application is pending? Give the approximate end date.
(g) If the application is approved, what is his new authorized stay end date? If it is denied after his I-94 date has passed, what must he do?

### Q4

(a) Tomás (Q3) filed his I-539 on December 1, 2027. He wants to visit home from December 22, 2027 to January 5, 2028. Can he make this trip without putting the pending I-539 at risk? Does it matter how he presents himself at re-entry? What, if anything, does the rule say he should carry?
(b) Separately, a different student has a pending application to *change* from F-1 to another nonimmigrant status and wants to travel abroad while it is pending. What does the rule say about this? Cite the provision.

### Q5

Mei is an F-1 master's student (D/S transition group) at School A, which issued her initial I-20; she began the master's there in August 2025. She will complete the master's on May 14, 2027 and has been admitted to a PhD program at School B starting August 23, 2027. Can her SEVIS record be transferred from School A to School B? Identify every provision in the final regulatory text that bears on the question, explain how each applies to her, and give your conclusion. Is there anything in the rule, or in later Federal Register documents, that could change your conclusion?

### Q6

Ahmed (D/S transition group) completes a master's degree on December 11, 2026 and does not apply for OPT. He wants to start an MBA (also a master's-level program) at another school in August 2027, either by transferring his SEVIS record or by leaving and re-entering on a new I-20.

(a) Can he obtain F-1 status for the MBA under either route? Cite the provisions that decide this.
(b) Separately from (a), what does the transfer timing rule say about an August 2027 start?
(c) Until what date is Ahmed authorized to remain after completing his master's (assume no other filings)?
(d) Could the answer to (a) change before August 2027? Explain.

### Q7

Lena is an F-1 PhD student in the U.S. A university (a cap-exempt employer) offers her a postdoc and will file an H-1B petition requesting a change of status, with a start date of July 1, 2027.

(a) A colleague says the "$100,000 H-1B payment" applies to her petition. Find the presidential document currently imposing that payment requirement and give its number, signing date, FR citation, effective date and expiration. Identify any other presidential documents that bear on it.
(b) Based on the text, does the payment requirement apply to Lena's petition? Could it reach her under other circumstances?
(c) Are there any DHS rulemakings in the Federal Register that would add fees for H-1B petitions? For each, give the amount, which petitions it covers, whether it would apply to Lena's petition, and its current status (including any corrections or later actions).
(d) If Lena's F-1 stay ends before July 1, 2027, does any F-1 provision automatically extend her status until the H-1B start date? Cite the current provision.
(e) If Lena travels abroad while the change-of-status request is pending, what happens to it?

### Q8

An adviser hears that "DHS is eliminating the 60-day grace period" and worries that Priya (Q2) will lose her 60-day departure period. Find the document behind this report and answer: (a) what it would change (cite the CFR paragraph) and whom it covers; (b) its status and any comment deadline; (c) whether it affects Priya's 60 days, and why; (d) whether it bears on any of the other students in this task.

### Q9

List at least five changes DHS made between the proposed rule and the final rule that affect F-1 students. For each, cite the paragraph of the final rule it touches and where in the Federal Register you found the change described.

### Q10

Between July 18, 2026 and today, which other Federal Register documents would matter to an F-1 student planning post-graduation work in the U.S.? For each, give the document number, type, publication date, a one-sentence summary of the relevant effect, and whether it is in force. Include at least four.

### Q11

An adviser is preparing a student handout and wants to include what an extension of stay costs and how long USCIS takes to decide it, based on the final rule. What does the final rule say on these points? Give the figures and where they appear, then draft one or two sentences the adviser could accurately put in the handout.

### Q12

Priya (Q2) asks two questions: (a) If USCIS receives her I-539 during the 60 days after her I-20 program end date, is it timely? (b) If she files during those 60 days, does she keep the automatic extension of on-campus or CPT employment while it is pending? Answer each, with your basis, and give the adviser a recommendation.

### Q13

Sofia was admitted in F-1 status for "D/S" in August 2023 and was maintaining status on September 15, 2026. Her I-20 shows a bachelor's program end date of May 14, 2027. She flies home on December 19, 2026 and is readmitted in F-1 status on January 9, 2027 with the same I-20. Her DSO will recommend her for post-completion OPT, and she will file Form I-765 on February 22, 2027, requesting OPT from June 10, 2027 through June 9, 2028.

(a) After her return, until what date is Sofia authorized to remain in the U.S. without filing anything? Name the provisions and show the arithmetic.
(b) Does she need to file a Form I-539 for the OPT period? If so, by when must USCIS receive it?
(c) If everything she files is approved as requested, until what date may she remain?
(d) Alternative facts: Sofia does not travel in December. She files the I-765 on February 22, 2027, completes her program on May 14, 2027, and visits home from May 20 to June 5, 2027 while the I-765 is still pending. Does she need a Form I-539? For what period may she be readmitted, and what should she carry?

### Q14

Daniel (D/S transition group; he has not left the U.S. since his last admission) holds a post-completion OPT EAD valid from July 1, 2026 through June 30, 2027, based on a master's degree in a STEM field. His DSO expects to recommend him for the 24-month STEM OPT extension in April 2027, and he would file Form I-765 on April 12, 2027. An adviser has heard that OPT "will soon cost $70,000, or $30,000 for an extension".

(a) Find the document behind this report. Give its document number, citation, type, agency, docket number, RIN and current status, including every deadline it sets.
(b) Suppose it were finalized as proposed and in effect before the DSO's April 2027 recommendation. Which amount would apply to Daniel's STEM OPT extension? Explain from the text.
(c) Under the proposal, who pays, at what point in the process, and what follows if the payment is not made? Is the payment refundable?
(d) Under the proposal, from when would the fee apply? Is there any timing of the DSO's recommendation that would keep Daniel outside it?
(e) Separately, under the rules in force today: what must Daniel file with USCIS for the STEM OPT period? What happens to his work authorization while it is pending, and until when may he stay if it is approved?

### Q15

An adviser has drafted seven statements about the final rule for a student newsletter. For each one, say whether it is correct, partly correct or incorrect, cite the provision or passage that decides it, and reword it if needed. Where the regulatory text and the preamble point in different directions, say so, say where, and say which controls.

1. "USCIS must receive an extension-of-stay application before the program end date on the student's I-20."
2. "The four-year maximum period of admission is counted from the day the student enters the United States."
3. "If USCIS has still not decided a timely filed extension application 240 days after the I-94 date, the student may stay and keep studying but must stop any on-campus job."
4. "A student in an English language training program who falls seriously ill can extend beyond 24 months on medical grounds."
5. "A degree program accredited as a five-year program has to be shortened, or issued on two I-20s, to fit the four-year limit."
6. "A student who travels abroad and is readmitted on an I-20 with a later program end date gets a new admission period from CBP, and then does not need an extension of stay from USCIS for that time."
7. "The exemption from filing Form I-539 for OPT applicants covers I-765s filed within six months of the rule's effective date, so the last filing day is March 15, 2027."

### Q16

Lin will begin a six-year PhD program. Her I-20 shows a program start date of August 23, 2027 and a program end date of May 14, 2033. She enters the U.S. in F-1 status on August 2, 2027, together with her husband in F-2 status.

(a) What admit-until date should Lin's I-94 show? Show the arithmetic.
(b) What must she do to stay beyond that date, what does she submit, and on what ground can it be granted? How early may she file? If it is granted in full, until what date may she stay?
(c) In 2029 her department awards her a master's degree on the way to the PhD. Does that affect her ability to finish the PhD in F-1 status under the rule's limits on programs at the same or a lower level?
(d) In August 2030 Lin spends three weeks abroad and is readmitted on her I-20. No extension application is pending. For what period may she be admitted, and does she still need the filing in (b)? Say how certain the answer is.
(e) Her husband travels separately in 2031, and his I-94 comes back with a later date than Lin's. Until when may he stay? How is he covered when Lin applies under (b), and what does the rule say about the fee?
