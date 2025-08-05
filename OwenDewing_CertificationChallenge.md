Owen Dewing  
AI Makerspace  
Certification Challenge  
Use Case: Student Loans

1. **Defining Problem and Audience**

* Problem: Most Americans don’t understand how the proposed changes in the student loan megabill will affect their financial obligations or repayment plans.

* Why this is a Problem: The Senate is proposing a new megabill that aims to overhaul how Americans borrow and repay student loans, which will affect students/graduates all across the US. If people are unaware of this bill, this could lead to misinformed economic and financial decisions, which could be detrimental, especially for students/graduates who are first-generation college students or in lower-income brackets. This application will be a place where users can get educated about the bill and get reliable information.

2. **Propose a Solution**

* Solution: The solution is a personalized Q\&A assistant that will use RAG and agentic reasoning to answer borrower-specific questions about the student loan megabill. Users can ask questions like:   
  * “What is the RAP plan and how does it work?”  
  * “How does this compare to SAVE or PAYE?”  
  * “Based on my income and debt, when would I be debt-free with this new plan?”

  The assistant includes a form where users can enter their loan amount, graduation year, and income. Based on this, the app generates a custom repayment timeline under the new RAP plan.

  The UI will look like a chatbot, with the title “Student Loan AI Assistant”. It will list its main services when users load the webpage, and will feel like a supportive and friendly assistant.

* Tech Stack Choices:

1. LLM: I will use the GPT-4.1-nano model for its cost-effective generation in RAG, and the gpt-4.1 model in the agent graph due to its reliable reasoning skills when choosing which tool to use.  
2. Embedding Model: I am using the *text-embedding-3-small* model due to its efficiency and cost-effectiveness.   
3. Orchestration: I am using LangGraph due to its ability to maintain state across retrieval and manage multi-step agent workflows.  
4. Vector Database: I am utilizing QDrant for this assignment because it is lightweight and integrates easily with LangChain/LangGraph. Furthermore, it is good for managing chunked legislative data.  
5. Monitoring: LangSmith is my choice for monitoring because it lets developers see and analyze every step of the evaluation process. It also tracks tool calls and is useful for debugging.  
6. Evaluation: RAGAS is the tool I am using to evaluate my golden testset and advanced retrieval methods due to its standardized metrics including faithfulness, recall, and precision.  
7. UI: React, CSS, and HTML are in charge of the UI and front-end of my application due to React’s simple component-based architecture and CSS’s design consistency and dynamic responsiveness.

* Agent Usage: My agent will be used to improve the performance of the responses and overall application through 5 tools.  
  * Tavily Search Tool: This tool will get the latest news/updates on the megabill and the student loan repayment plan (RAP).  
  * Tool Comparison Tool: This tool is an expert at knowing the existing loan repayment plans (SAVE, PAYE, IBR, etc), and will be utilized when the user asks about comparing an existing plan to the proposed RAP plan.  
  * Compile Form Tool: Accepts user loan information and reformats it into a structured input for the timeline simulation.  
  * Timeline Tool: This tool will utilize the form output to generate a timeline that the user can follow to pay off their student loans under the new RAP plan.

3. **Dealing with the Data**

   

* RAG Data Sources  
  * Official Documents: I wanted to add official documents to my application to give users the most accurate and up-to-date information.  
    * The official Big Beautiful Bill: [https://www.congress.gov/bill/119th-congress/house-bill/1/text](https://www.congress.gov/bill/119th-congress/house-bill/1/text)  
    * Section-by-section explanation from U.S. Senate Finance Committee of megabill: [https://www.finance.senate.gov/imo/media/doc/finance\_committee\_section-by-section\_title\_vii5.pdf](https://www.finance.senate.gov/imo/media/doc/finance_committee_section-by-section_title_vii5.pdf)  
  * Past and current repayment plans: For the tool comparison tool, I wanted to add documents displaying past and current repayment plans so users can learn how to adjust to the new RAP plan.  
    * SAVE plan: [https://edfinancial.studentaid.gov/income-driven-repaymentinformation-center/save](https://edfinancial.studentaid.gov/income-driven-repaymentinformation-center/save)  
    * IBR and PAYE plans: [https://images2.americanprogress.org/campus/GenerationProgress/PAYE\_IBR\_Fact\_Sheet.pdf](https://images2.americanprogress.org/campus/GenerationProgress/PAYE_IBR_Fact_Sheet.pdf)  
    * IDR plan: [https://studentaid.gov/sites/default/files/IncomeDrivenRepayment-en-us.pdf](https://studentaid.gov/sites/default/files/IncomeDrivenRepayment-en-us.pdf)  
    * Direct Loan Program: [https://fsapartners.ed.gov/knowledge-center/fsa-handbook/2025-2026/vol8](https://fsapartners.ed.gov/knowledge-center/fsa-handbook/2025-2026/vol8)  
  * Other documents:  
    * Federal Student Loan Repayment Plans: [https://studentaid.gov/manage-loans/repayment/plans](https://studentaid.gov/manage-loans/repayment/plans)  
    * Megabill summary: [https://www.highereddive.com/news/higher-education-measures-senate-reconciliation-bill/752131/?utm\_source=chatgpt.com](https://www.highereddive.com/news/higher-education-measures-senate-reconciliation-bill/752131/?utm_source=chatgpt.com)  
* External APIs  
  * Tavily Search API: Real-time web search for bill updates, commentary, and interpretations.  
  * Arxiv API: I am utilizing this API to …  
* For chunking, I am using the *RecursiveCharacterTextSplitter* with a chunk size of 1000 and an overlap of 200\. The 1000-token chunks give enough context for legal documents, and the 200 token overlap helps with continuity between chunks.  
4. **Building a Quick End-to-End Agentic RAG Prototype**

Check README to see instructions on how to run and watch Loom video for demo.

5. **Creating a Golden Test Data Set**

| metric | score | analysis |
| :---- | :---- | :---- |
| context\_precision | 1.000 | 100% of the retrieved documents are relevant |
| faithfulness | .6500 | 65% of the answer content comes from the retrieved documents. This means that around 35% of answers may be hallucinated, or from other external knowledge. This could be improved. |
| Answer relevancy | .6573 | 65.73% of the answers are relevant to the questions. Around 34% of the answers miss the mark and are irrelevant. This could also use improving. |
| context\_entity\_recall | .2110 | Only 21.1% of the important entities from the question are being retrieved. This means that users might not get complete answers, and it could definitely be improved. |

My pipeline is pretty good at filtering out irrelevant content and finding relevant documents. However, a lot of the answers are at risk of being hallucinations. There is also incomplete coverage and users might not get complete answers about certain topics. To improve this, I could increase the retrieval size from 10 to 15-20, use smaller chunks for better topic capturing, or make the RAG prompt more strict.

6. **The Benefits of Advanced Retrieval**

My retrieval techniques:

* Contextual Compression (Rerank): I am choosing this retrieval method because this is the method that performed the best on the previous homework assignment. Also, contextual compression is good because it reranks and compresses retrieved documents to preserve only the important and relevant chunks.   
* Parent Document Retrieval: I want to use this retrieval method because a lot of my documents are long and hierarchical (especially the official government documents), and this retriever returns larger parent sections when retrieving smaller chunks, helping preserve the full context.

7. **Assessing Performance**

| metric | baseline | contextual\_compression | parent\_document |
| :---- | :---- | :---- | :---- |
| context\_precision | 1.000 | .8454 | .9861 |
| faithfulness | .6500 | .9815 | .7325 |
| Answer relevancy | .6573 | .6391 | .6335 |
| context\_entity\_recall | .2110 | .5591 | .4750 |

Overall, these results show that the baseline retriever is precise, but cuts out important topics and background, hurting the overall accuracy. Contextual compression increases both faithfulness and entity recall significantly, and it looks like the best option out of the three. The parent document retriever also has high context precision and faithfulness, and is also a better option then the baseline. Nevertheless, answer relevancy and context entity recall are pretty low across the board, and can definitely be improved through more testing.

* Changes to app:  
  * I hope to come up with a more creative use case. I didn’t get started on this challenge early enough, and defaulted to the class use case. I want to create an application with a topic that I’m passionate about, like maybe music production or music listening analysis.  
  * I want to find a use case for developing a multi-agent pipeline. It didn’t really make sense for an app with this small of a scope, but is definitely something I’m interested in.  
  * I found myself more drawn to working with agentic reasoning and tool use than with RAG pipelines. I want to expand on this by creating more complex custom tools.  
  * I want to utilize more detailed chunking methods. For example, if I had more time in this assignment, I could have chunked the official legislative documents by header sections, and the other documents with standard overlap.