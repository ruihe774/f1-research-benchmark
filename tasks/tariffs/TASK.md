# Policy Research Task: The 2026 Duties on Canadian Products and the Forced-Labor Tariffs

## Your role

You are a policy researcher on the trade compliance team of a U.S. customs brokerage. Brokers bring you shipments and client questions. Your job is to find the governing federal documents, read them carefully, and give answers that a broker could check line by line.

Two sets of 2026 actions matter for this task:

- the President's actions under **section 338 of the Tariff Act of 1930** against products of Canada (alcoholic beverages, dairy and motor vehicles), and every later document that delayed, changed or added to them; and
- the U.S. Trade Representative's July 2026 action under **section 301 of the Trade Act of 1974** in the investigations of forced-labor import prohibitions, together with the presidential document directing it and the earlier proposal.

**Today's date is November 14, 2026.** Treat the Federal Register as of today as the state of the world.

## Your tools

You have five function tools. All of them search and read the U.S. Federal Register (rules, proposed rules, notices, and presidential documents):

- `fr_search`: search documents by keywords and filters (document type, agency, publication date range, docket, RIN, CFR part, sort order, paging).
- `fr_doc`: metadata for one document: dates, citation and page range, docket, RIN, CFR parts affected, corrections.
- `fr_toc`: outline of a document's headings, with line numbers.
- `fr_grep`: regex search inside one document's full text, with context lines and the FR page of each match.
- `fr_text`: read a document's full text by line range.

Documents are identified by their FR document number (e.g. 2024-00366), which `fr_search` returns. Long documents are easiest to navigate with `fr_toc`, then `fr_grep`, then `fr_text`; presidential documents often have no headings, so read them with `fr_text`. In full text, `[[Page N]]` markers give FR page numbers. Tool output sometimes contains command-line hints such as "continue with --start 1201"; these refer to the tool's parameters (here, `start`).

**Annexes are not readable.** The annexes of these documents (product lists and the tables of new tariff headings) were published as images, and the tools show only a placeholder for each image. Each scenario below therefore tells you which annex list a product is on. Rules that appear only in an image are outside this task; if an answer depends on one, say so.

**Limits.** This conversation has a context budget: a fixed number of tokens for everything you read and write, including tool results. Every tool result ends with a line giving the approximate number of tokens left. When the budget is used up, tool calls are disabled and you are asked for your final answer based on what you have found, so plan your reading against it. There is also a turn limit, which is generous.

You have no other tools: no web browsing, no other databases (the Harmonized Tariff Schedule, CBP messages and agency websites are not available). Do not rely on memory for facts about documents published in 2025–2026. If something cannot be established from the Federal Register, say so.

## Ground rules

1. **Cite everything.** For every factual claim, cite the FR document number and, where possible, the numbered clause, section or note subdivision (e.g. "clause (3) of Proclamation 10000, FR Doc. 2024-00366") or the FR page (e.g. "89 FR 17062").
2. **Separate the kinds of authority.** Distinguish (a) operative text (the numbered clauses of a proclamation, the sections of a memorandum, the text of a tariff-schedule note, the DATES line of a notice), (b) recitals and preamble explanation, (c) statements made by commenters, and (d) proposals that were not adopted as proposed.
3. **Say when the text is silent.** If the documents do not answer a question, say so plainly, give the most defensible reading, and explain the uncertainty. A confident answer that the text does not support is worse than a clearly flagged gap.
4. **Show the arithmetic.** For every duty amount, show the value, the rate and the result, one line per duty layer, and then the total asked for.
5. **Do not give legal advice.** Write as a research memo for a broker, not as instructions to an importer.

## Answer format

When your research is done, give your final answer in the structured format you are given: one entry per question (Q1, Q2, ...), each with three fields:

- **answer:** the direct answer to each lettered part, in order, labelled (a), (b), ...
- **basis:** the provisions and documents relied on, with citations.
- **uncertainty:** anything the documents leave open (write "None" if nothing).

Markdown is fine inside the fields. Each answer must stand on its own: brokers read them separately, so repeat a point rather than refer to another question's answer.

## Assumptions for every scenario

Unless a scenario says otherwise:

- Goods are products of the country named, and are commercial shipments.
- A product is on the annex lists the scenario names and on no other list that was published as an image, in any document in this task. Whether a rule or exemption that is readable as text applies is for you to work out. Where a scenario gives a tariff subheading, the article is classified there and matches the subheading's description.
- No trade-agreement preference is claimed, no chapter 98 provision is used, and no section 232 duty, antidumping duty, countervailing duty or other additional duty applies. A scenario that names a section 232 duty or heading overrides this for that duty.
- "MFN rate" means the column 1-General rate of duty, which the scenario gives. Values are customs values in U.S. dollars.
- Times are Eastern. An event dated without a time happened during business hours that day. "Arrives" means the goods physically arrive at a U.S. port and are imported at that moment.
- "Section 338 duty" means a duty under the Canada actions; "section 301 duty" means a duty under the forced-labor action only. Ignore merchandise processing fees and other user fees.

---

## Questions

### Q1

List every presidential document in the section 338 series against Canada published through today. For each give the proclamation number, the FR document number, the FR citation (first page), the date signed, the date published, one line on what it does, and the date and time from which its operative change applies. Say which kind of event that date and time is measured against in each document. Then say, for each of the three product groups, which documents changed which products are subject to the duty.

### Q2

An importer made three consumption entries of Canadian wine that is listed in Annex II of the alcoholic-beverages duty proclamation. Entry 1 was made at 2:00 p.m. on August 20, 2026; entry 2 at 11:59 p.m. on August 21; entry 3 at 12:01 a.m. on August 22. Each has a customs value of $40,000.

(a) How much section 338 duty is owed on each entry? Cite the controlling text.
(b) The duty proclamation itself prints a different start date. Explain exactly how the start date was changed: which text was amended, which was not, and what resolves the difference.
(c) On entry 1 the broker deposited the 50 percent duty. What do the documents say about getting it back?
(d) Did the duties need a further presidential action in order to begin? What do later documents say happened in the days before they began?
(e) Why was the original start date the date it was? Show the arithmetic from the text.

### Q3

A Canadian bottled beer is listed in Annex II of the alcoholic-beverages duty proclamation, was not touched by the alcoholic-beverages scope modification, and is listed in the Annex of the alcoholic-beverages import exclusion proclamation. Each shipment has a customs value of $30,000; the MFN rate is free.

(a) For each shipment, say whether it may be imported and how much section 338 duty is owed:

- A. Arrives September 10, 2026; entered for consumption September 14.
- B. Arrives September 27; placed in a bonded warehouse; withdrawn from the warehouse for consumption October 5.
- C. Arrives at 11:30 p.m. on September 28; consumption entry filed at 9:00 a.m. on September 29.
- D. Arrives at 12:30 a.m. on September 29; the importer wants to file a consumption entry that morning.

(b) Shipment E arrives September 25 and is admitted to a foreign trade zone that day. The importer wants to enter it for consumption from the zone on October 6. What duty or restriction applies?
(c) Suppose a court later holds the import exclusion invalid as applied to this beer. What applies to shipments of it imported after that ruling, and under which provision?
(d) Does the exclusion proclamation change the duty on listed Canadian alcoholic products that are not in its Annex?

### Q4

Three Canadian products are each subject to a 25 percent ad valorem duty under section 232 of the Trade Expansion Act, assessed on the full customs value (assume this throughout). Product X is listed in Annex II of the alcoholic-beverages duty proclamation, product Y in Annex II of the dairy duty proclamation, and product Z in Annex II of the motor-vehicles duty proclamation. None of them is on any other list. Each shipment has a customs value of $100,000.

(a) For consumption entries made on September 10, 2026, give the section 232 duty and the section 338 duty on X, Y and Z.
(b) Do the same for consumption entries made on October 1, 2026.
(c) Quote or cite the exact text that decides each answer, with the FR page.

### Q5

Four Canadian products, none of them subject to a section 232 duty or to an import exclusion:

- P is listed in Annex I, Part A of the September motor-vehicles scope proclamation. It was not listed in the original motor-vehicles duty proclamation.
- Q is listed in Annex II of the original motor-vehicles duty proclamation and in Annex I, Part B of the September scope proclamation.
- R is listed in Annex II of the original motor-vehicles duty proclamation and in Annex I, Part A of the October scope proclamation.
- S is listed in Annex I, Part B of the October scope proclamation. It was not listed in any earlier document.

(a) For each product, say whether the 50 percent duty applies to a consumption entry made at each of these five times: 3:00 p.m. on September 14; 12:01 a.m. on September 15; 4:00 p.m. on October 29; 12:01 a.m. on October 30; November 3. Explain the basis for each product.
(b) For the October scope proclamation, give the dates it was signed, filed with the Office of the Federal Register, and published, and the time from which it applies. Do the scope proclamations reach entries made before they apply, and do they provide for refunds?
(c) As these documents describe section 338, there is a waiting period before additional duties may take effect. How long after signing did P and S become dutiable, and do the scope proclamations explain how that fits the waiting period?

### Q6

A product has an MFN rate of 4 percent ad valorem. A shipment with a customs value of $100,000 is entered for consumption in September 2026.

(a) Give the section 301 duty, and the total of MFN duty plus section 301 duty, if the shipment is a product of: (1) Switzerland; (2) Norway; (3) the United Kingdom; (4) Germany; (5) Taiwan; (6) Türkiye; (7) Japan; (8) Liechtenstein; (9) Hong Kong; (10) India.
(b) Give the section 301 duty only, on the same $100,000, for: a product of Germany with an MFN rate of 12 percent; a product of Japan with an MFN rate of 12 percent; a product of Taiwan with an MFN rate of exactly 10 percent; a product of South Korea with an MFN rate of exactly 10 percent; and a product of Switzerland that is MFN duty-free.
(c) For which of the ten economies in (a) does the adopted treatment differ from what was proposed in June 2026, and how? For any economy whose rate itself changed, give the reason the documents state.

### Q7

(a) A product of France has a column 1-General rate of 3 cents per kilogram. A shipment weighs 2,000 kg and has a customs value of $12,000. What is the section 301 duty?
(b) A product has a column 1-General rate of 4 percent plus 25 cents per kilogram. A shipment weighs 4,000 kg and has a customs value of $20,000. What is the section 301 duty if it is a product of Italy? Of Japan? Of Brazil?
(c) On a shipment with a customs value of $20,000, the duty payable under column 1-General is $2,200. What is the section 301 duty if it is a product of Taiwan? Of Switzerland?
(d) Where is the rule for treating MFN rates that are not ad valorem stated, and where is the result for an equivalent rate at or above the cap stated?

### Q8

Each shipment below is a product of the Dominican Republic with a customs value of $80,000; the MFN rate is free.

(a) What section 301 duty is owed on each?

1. Loaded on a vessel at the port of Caucedo on July 22, 2026, sailing directly to Miami; entered for consumption on July 29.
2. Same sailing; entered for consumption at 3:00 p.m. on July 27.
3. Same sailing; entered for consumption at 12:01 a.m. on July 28.
4. Loaded on a vessel at Caucedo at 6:00 a.m. on July 24, sailing directly to Miami; entered for consumption on July 27.
5. Entered for consumption on July 23.
6. Arrived in June and held in a bonded warehouse since; withdrawn from the warehouse for consumption on July 26.
7. Air freight: loaded on an aircraft in Santo Domingo at 9:00 p.m. on July 23, flown directly to Miami; entered for consumption on July 25.

(b) Cite exactly where the rule for goods in transit is stated.
(c) Give the date the presidential document was signed, the date and time from which the duties apply, and the date the action was published.
(d) A patented pharmaceutical article that is a product of the Dominican Republic, provided for in heading 9903.04.62 of the tariff schedule, with a customs value of $80,000: what section 301 duty is owed if it is entered for consumption on July 30, 2026? On August 3, 2026?

### Q9

What section 301 duty is owed in each case?

(a) A machine assembled in Thailand is entered under heading 9802.00.80. The value of the assembled article is $100,000, which includes U.S.-made components worth $35,000.
(b) A U.S.-made machine worth $150,000 is returned from Israel after repairs there that cost $6,000, and is entered under subheading 9802.00.50. Treat the repairs as a product of Israel.
(c) A product of Mexico with an MFN rate of 5 percent and a customs value of $50,000: (i) entered free of duty under the USMCA; (ii) entered with no USMCA claim.
(d) A passenger car that is a product of Japan, entered under section 232 heading 9903.94.01, customs value $40,000.
(e) A product of Brazil with a customs value of $100,000 that is subject to a section 232 duty under a chapter 99 heading that the section 301 note does not mention.
(f) What did the June 2026 proposal say about goods subject to section 232 duties, and about informational materials and donations? What does the adopted text say on each?

### Q10

Scenario 1. Canadian aluminum extrusions have been listed in Annex II of the motor-vehicles duty proclamation since it was signed, and are on no Part A, Part B or exclusion list. They are subject to a 50 percent section 232 duty on the full customs value and are entered under section 232 heading 9903.82.02. The MFN rate is 3 percent, the customs value is $200,000, and no USMCA claim is made. Give each duty layer (MFN, section 232, section 338, section 301) and the total for a consumption entry on:

(a) September 10, 2026;
(b) September 16, 2026.

Scenario 2. Canadian rye whisky in bottles is listed in Annex II of the alcoholic-beverages duty proclamation, was not touched by the scope modification, and is listed in the Annex of the alcoholic-beverages import exclusion proclamation. The MFN rate is free and the customs value is $60,000. Give the section 338 duty, the section 301 duty and their total for:

(c) a consumption entry on September 1, 2026, entered free of duty under the USMCA;
(d) a consumption entry on September 1, 2026, with no USMCA claim;
(e) a shipment that arrives on October 2, 2026.

(f) A client asks whether Canadian goods entered in September 2026 also bear a duty under the International Emergency Economic Powers Act (the Canada "northern border" duties) or the 10 percent temporary import surcharge. Answer from the Federal Register, with the documents and dates.

### Q11

The documents of each action do not always agree with one another, or with themselves. In the documents of the section 301 forced-labor action and of the section 338 actions against Canada, find places where a statement in one document about what the action provides, or about what another document of the same action says or does, differs from the operative text of that document or of the other document. For each, quote or closely paraphrase both sides and give the document and FR page of each. List as many as you can find, and list each discrepancy once. A change between the June proposal and the adopted text is not in itself a discrepancy; it is one only where a document describes the proposal or the adopted text inaccurately. Do not list matters on which a document is merely silent, or content published only as an image.

### Q12

Each shipment below is entered for consumption on September 10, 2026. What section 301 duty is owed on each?

(a) Aloe, Tasmanian pepper, coconut and centella extracts (subheading 1302.19.91), customs value $60,000, MFN rate free: as a product of Cambodia; as a product of Malaysia.
(b) Boswellia (subheading 1301.90.91), customs value $100,000, MFN rate free: as a product of Malaysia; of Taiwan; of Bangladesh; of Argentina.
(c) Argan oil (subheading 1515.90.81), customs value $100,000, MFN rate 4 percent: as a product of Taiwan; of Japan; of Indonesia.
(d) Sesame seeds for sowing (subheading 1207.40.00), customs value $50,000, MFN rate 2 percent: as a product of Japan; of Mexico; of Thailand.
(e) Psyllium seed husks (subheading 1211.90.89), customs value $40,000: as a product of Cambodia (MFN free); of Thailand (MFN free); of El Salvador (MFN free); of Italy (MFN rate 2 percent).

### Q13

A plant in Canada builds a mobile industrial machine. Assume that the machine is a steel article listed in Annex I-C of the June 2026 proclamation that modified the section 232 duties on aluminum, steel and copper; that most of the steel and aluminum in it, by weight, was melted or smelted outside the United States; that it is on no section 338 list; and that no program for approved onshoring plans covers it. Each unit has a customs value of $200,000. The MFN rate is free unless stated. Give the section 232 duty only. Each unit is entered for consumption on October 20, 2026 unless another date is given.

(a) A product of Canada that qualifies for preferential treatment under the USMCA and is entered with a USMCA claim. Parts produced in the United States account for $60,000 of its value.
(b) As in (a), but with no U.S. content of any kind.
(c) A product of Canada that does not qualify for USMCA treatment. Parts produced in the United States account for $60,000 of its value.
(d) The same machine built in Japan, a product of Japan, with an MFN rate of 2.5 percent.
(e) As in (a), except that parts produced in the United States account for $20,000 of its value, and a further $30,000 of its value is attributable to aluminum smelted and cast in the United States that is contained in a part made in Canada.
(f) As in (e), but entered for consumption on October 6, 2026.
(g) As in (a), except that parts produced in the United States account for $140,000 of its value.
(h) Until when does the treatment in (a) apply, and what applies afterwards?

### Q14

A law firm's client alert about the forced-labor action makes the ten statements below. For each one, say whether it is correct, partly correct or incorrect, and give the passage or passages that decide it, with the document and FR page. Where the documents of this action differ from one another, say which document says what.

1. "The memorandum gives USTR until September 1, 2026 to set up the textile tariff-rate quotas."
2. "USTR received over 450 written comments on the proposed action and heard nearly 60 witnesses."
3. "After the June proposal, seven economies were moved from 12.5 percent to 10 percent because each of them adopted a forced-labor import ban."
4. "In response to comments linking them to forced labor, USTR removed beef and avocados from the list of exempt products."
5. "Every economy whose rate is net of the MFN rate also has its own negotiated list of exempt products."
6. "USTR exempted 471 more products than it had proposed, including all sugar and sugar-containing products."
7. "USTR stated that no product will bear more than 12.5 percent duty in total."
8. "Goods admitted to a foreign trade zone once the duties apply must be admitted in privileged foreign status, unless they are eligible for domestic status."
9. "If a court holds one of the exemptions invalid, the goods it covered become subject to the duty."
10. "Of the products on the proposal's list of exempt products (its Annex A), the only ones USTR cut back were certain chemicals."

### Q15

A customs audit covers consumption entries of aluminum extrusions (bars, rods and profiles of heading 7604) that are products of Canada. Each entry has a customs value of $100,000, all of it aluminum. Assume that throughout the period the extrusions are an aluminum article within the section 232 aluminum duties (in 2026, listed in Annex I-A of the April proclamation on aluminum, steel and copper and not in Annex I-C of the June proclamation); that they have been listed in Annex II of the section 338 motor-vehicles duty proclamation since it was signed and are on no Part A, Part B or exclusion list; that no reduction granted to a particular producer or under an approved plan applies; and that no exemption exists other than those readable as text. From April 6, 2026 the extrusions are entered under section 232 heading 9903.82.02. The general assumption that no other additional duty applies does not hold for this question: every additional duty that the Federal Register imposed on these goods on the entry date counts. Give the duties legally owed on each entry as the Federal Register stands today.

For each entry date below, give every duty owed in addition to the MFN duty, by legal authority, with the amount and the total, and for each other additional duty then in force on products of Canada, say in a line why it is not owed. Do this for two cases. Case N: the goods do not qualify for USMCA treatment. Case U: the goods qualify for USMCA treatment and are entered with a USMCA claim.

1. February 10, 2025
2. March 6, 2025
3. March 10, 2025
4. March 14, 2025
5. June 3, 2025
6. June 10, 2025
7. August 5, 2025
8. March 2, 2026
9. June 10, 2026
10. July 27, 2026
11. August 25, 2026
12. September 14, 2026
13. September 16, 2026
14. November 10, 2026
