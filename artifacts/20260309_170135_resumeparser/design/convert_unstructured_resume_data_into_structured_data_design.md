# Software Design Specification for US-002: Convert unstructured resume data into structured data

## 1. Component Scope

This component is designed to process unstructured resume data and convert it into structured data. The component will accept resumes in various formats such as PDF, DOC, DOCX, and plain text. The output will be a standardized JSON format containing candidate information.

## 2. Architecture and Interfaces

### Components

1. **Resume Parser**: This component will be responsible for extracting data from unstructured resume files. It will support various file formats and use Optical Character Recognition (OCR) for PDF and image-based resumes.
2. **Data Processor**: This component will clean, normalize, and transform the extracted data into a structured format. It will ensure data consistency and validate data against predefined rules.
3. **Data Storage**: This component will store the structured data in a database for easy search and retrieval.
4. **API Gateway**: This component will provide an API for external applications to access the structured data.

### Interfaces

#### Input Interfaces

- Resume Parser: Accepts unstructured resume data in various formats.
- API Gateway: Accepts requests for structured data from external applications.

#### Output Interfaces

- Data Processor: Provides structured data to the Data Storage component.
- API Gateway: Provides structured data to external applications.

## 3. Data Contracts

The structured data will include the following fields:

- **Candidate ID**: Unique identifier for each candidate.
- **Name**: Full name of the candidate.
- **Contact Details**: Email address and phone number.
- **Education**: Degree, major, graduation year, and institution.
- **Skills**: List of skills.
- **Work Experience**: Company name, job title, start and end dates, and job description.
- **Certifications**: Name, issuing organization, and issue date.

## 4. Risks and Mitigations

### Risks

- **Data Extraction**: Inaccurate or incomplete data extraction from unstructured resumes.
- **Data Validation**: Incorrect or inconsistent data in the structured data.
- **Data Security**: Unauthorized access to sensitive candidate information.

### Mitigations

- **Data Extraction**: Use advanced OCR and machine learning algorithms for data extraction. Implement error handling and retries to improve accuracy.
- **Data Validation**: Implement data validation rules and data normalization techniques to ensure data consistency.
- **Data Security**: Implement access control and encryption to protect sensitive candidate information.

## 5. Non-functional considerations

### Performance

- The component should be able to process and convert 100 resumes per second.
- The API Gateway should respond within 100ms for 95% of requests.

### Scalability

- The component should be horizontally scalable to handle increased load.
- The database should be able to store data for 1 million candidates.

### Availability

- The component should be available 99.9% of the time.
- The API Gateway should have a 99.9% uptime SLA.