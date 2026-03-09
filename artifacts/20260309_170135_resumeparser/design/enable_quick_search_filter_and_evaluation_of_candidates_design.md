# Software Design Specification for US-003: Enable quick search, filter, and evaluation of candidates

## 1. Component Scope

This component is designed to enhance the recruitment system by enabling quick search, filter, and evaluation of candidates based on extracted and organized data. The following components will be included in this design:

- **Search Engine:** A powerful search engine to index and search resumes based on extracted data.
- **Filtering System:** A system to apply filters on search results based on extracted data.
- **Evaluation Dashboard:** A dashboard for recruiters to evaluate candidates based on extracted data.

## 2. Architecture and Interfaces

![Architecture Diagram](architecture.png)

**Components:**

1. **Recruitment System:** The core recruitment system where resumes are stored.
2. **Data Extraction Module:** Extracts data from resumes and stores it in the search index.
3. **Search Engine:** Indexes and searches resumes based on extracted data.
4. **Filtering System:** Applies filters on search results based on extracted data.
5. **Evaluation Dashboard:** Displays search results and allows recruiters to evaluate candidates.

**Interfaces:**

1. **Data Extraction Module <-> Recruitment System:** The data extraction module interacts with the recruitment system to extract data from resumes.
2. **Search Engine <-> Filtering System:** The search engine sends search results to the filtering system.
3. **Filtering System <-> Evaluation Dashboard:** The filtering system sends filtered results to the evaluation dashboard.

## 3. Data Contracts

**Resume Data:**

- `id`: A unique identifier for each resume.
- `data`: A JSON object containing extracted data.

**Search Result:**

- `id`: A unique identifier for each search result.
- `resume_id`: The id of the resume.
- `score`: A score indicating the relevance of the resume to the search query.

**Filter:**

- `field`: The data field to filter on.
- `operator`: The filtering operator (e.g., "equals", "greater_than", "less_than").
- `value`: The value to filter on.

## 4. Risks and Mitigations

**Risk:** Inaccurate data extraction may lead to incorrect search results.
**Mitigation:** Implement data validation and error handling in the data extraction module.

**Risk:** High volume of search queries may impact system performance.
**Mitigation:** Implement caching and indexing to improve search performance.

## 5. Non-functional considerations

**Performance:** The system should be able to handle a large volume of resumes and search queries without significant degradation in performance.

**Scalability:** The system should be able to scale horizontally to handle increased load.

**Security:** The system should ensure data privacy and security, particularly with regard to resume data.