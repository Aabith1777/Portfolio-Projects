import json
import os

prompts = []

# --- 1. RESUME PROMPTS (id: res-001 to res-010) ---
res_data = [
    {
        "id": "res-001",
        "title": "Professional Summary Storyteller",
        "category": "resume",
        "difficulty": "Intermediate",
        "description": "Crafts a compelling 3-4 sentence resume summary that focuses on impact and career alignment rather than generic lists of skills.",
        "tags": ["Summary", "Storytelling", "Introduction"],
        "prompt": "Create a professional resume summary based on my background. Structure it in 3-4 sentences: Sentence 1: My core identity, years of experience, and main value proposition. Sentence 2: My biggest quantitative achievement or signature skill in action. Sentence 3: The unique approach/philosophy I bring to solving problems. Sentence 4: My career objective and what value I intend to deliver in my next role. Here is my raw experience: [YOUR_EXPERIENCE] and the target role is [TARGET_ROLE].",
        "exampleInput": "YOUR_EXPERIENCE: 8 years in digital marketing, led a team of 3, managed $50k monthly ad spend, increased lead gen by 40% last year, pivoting from B2C to B2B SaaS.\nTARGET_ROLE: Senior B2B Marketing Manager",
        "exampleOutput": "Driven Digital Marketing Leader with over 8 years of experience spearheading high-impact campaigns and managing cross-functional teams to accelerate brand growth. Demonstrated success in managing $50k monthly ad spends and scaling lead generation pipelines by 40% through rigorous data-driven experimentation. Combines creative storytelling with deep marketing analytics to build high-converting B2B buyer journeys. Poised to leverage B2C conversion strategies to accelerate pipeline velocity and customer acquisition for your B2B SaaS platform.",
        "tips": ["Keep it under 100 words.", "Avoid passive voice.", "Align your core identity directly with the target job title."]
    },
    {
        "id": "res-002",
        "title": "X-Y-Z Resume Bullet Points Re-writer",
        "category": "resume",
        "difficulty": "Advanced",
        "description": "Applies Google's X-Y-Z formula (Accomplished [X] as measured by [Y], by doing [Z]) to transform weak bullet points.",
        "tags": ["Bullet Points", "Google Formula", "Quantitative"],
        "prompt": "Rewrite the following resume bullet point using Google's X-Y-Z formula: 'Accomplished [X] as measured by [Y], by doing [Z]'. Ensure it starts with a strong action verb, includes a clear metric of success, and details the specific technology or methodology used. Here is my current bullet point: [BULLET_POINT] and here is the context: [CONTEXT].",
        "exampleInput": "BULLET_POINT: I was in charge of updating the company database to make it faster.\nCONTEXT: PostgreSQL database, reduced query load times from 5 seconds to 0.8 seconds, optimized indexing and query structure.",
        "exampleOutput": "Optimized database query performance by 84%, reducing average load latency from 5s to 0.8s, by restructuring SQL queries and implementing multi-column indexes in PostgreSQL.",
        "tips": ["Start with a past-tense action verb.", "Be specific about the tool or tech stack used.", "Put the result first to catch the eye."]
    },
    {
        "id": "res-003",
        "title": "Technical Skills Categorizer",
        "category": "resume",
        "difficulty": "Beginner",
        "description": "Organizes a messy list of technologies, frameworks, and methodologies into clean, professional groups.",
        "tags": ["Technical Skills", "Formatting", "Clarity"],
        "prompt": "Take my disorganized list of technical skills and organize them into professional categories suitable for a resume (e.g., Languages, Frameworks & Libraries, Tools & Databases, Methodologies). Remove any redundant or obsolete skills. List: [SKILLS_LIST] and Target Domain: [TARGET_DOMAIN].",
        "exampleInput": "SKILLS_LIST: Python, HTML, Git, VS Code, Django, Postgres, React, Agile, Scrum, Docker, Jira, CSS, Flask, Excel, Word, JavaScript.\nTARGET_DOMAIN: Full-Stack Web Development",
        "exampleOutput": "• Languages: JavaScript, Python, HTML5, CSS3\n• Frameworks & Libraries: React, Django, Flask\n• Databases & Tools: PostgreSQL, Docker, Git, VS Code, Jira\n• Methodologies: Agile, Scrum",
        "tips": ["Don't list standard office tools like Excel or Word unless specifically relevant to the role.", "Group by proficiency or role relevance."]
    },
    {
        "id": "res-004",
        "title": "Career Pivot Alignment Optimizer",
        "category": "resume",
        "difficulty": "Advanced",
        "description": "Aligns a resume with a completely new industry or role by framing transferable skills in the target industry's language.",
        "tags": ["Career Transition", "Transferable Skills", "Positioning"],
        "prompt": "Help me rewrite my experience to highlight transferable skills for a career transition. I am moving from [CURRENT_ROLE/INDUSTRY] to [TARGET_ROLE/INDUSTRY]. Take my experience bullet points: [PAST_EXPERIENCE] and rephrase them using the vocabulary, priorities, and metrics of the target industry.",
        "exampleInput": "CURRENT_ROLE/INDUSTRY: High School Teacher\nTARGET_ROLE/INDUSTRY: Corporate Instructional Designer / Corporate Trainer\nPAST_EXPERIENCE: Designed weekly lesson plans for 120 students, graded papers, held parent-teacher conferences, used Google Classroom.",
        "exampleOutput": "• Designed and developed curriculum and learning paths for 120 learners, ensuring alignment with performance objectives and assessment metrics.\n• Facilitated high-engagement training modules utilizing LMS platforms (Google Classroom) to track learner progression and compliance.\n• Managed stakeholder communications and feedback loops, translating complex educational outcomes into clear performance reports.",
        "tips": ["Translate 'students' to 'learners', 'lesson plans' to 'curriculum design', and 'grading' to 'assessment metrics'."]
    },
    {
        "id": "res-005",
        "title": "Executive Presence Enhancer",
        "category": "resume",
        "difficulty": "Advanced",
        "description": "Upgrades regular operational resume bullets into strategic, business-impacting leadership achievements.",
        "tags": ["Executive Resume", "Leadership", "Business Impact"],
        "prompt": "Revise these resume bullet points to emphasize strategic thinking, leadership, cross-functional collaboration, and fiscal responsibility instead of just task execution. Shift focus from 'doing' to 'leading' and 'influencing'. Bullet points: [BULLET_POINTS] and Target Executive Title: [TARGET_TITLE].",
        "exampleInput": "BULLET_POINTS: Managed the development team, ran daily standups, worked on project timelines, kept eye on project budgets.\nTARGET_TITLE: Director of Engineering",
        "exampleOutput": "• Spearheaded engineering execution across cross-functional product teams, driving on-time delivery of major feature releases.\n• Established agile delivery frameworks that reduced cycle time by 18% and improved cross-departmental collaboration.\n• Managed capital budgets and resource allocation, optimizing headcounts to align with enterprise strategic roadmaps.",
        "tips": ["Use words like 'spearheaded', 'orchestrated', 'pioneered', and 'championed'.", "Link actions directly to high-level company goals."]
    },
    {
        "id": "res-006",
        "title": "Freelance to Corporate Translator",
        "category": "resume",
        "difficulty": "Intermediate",
        "description": "Presents independent contract work and freelance projects under cohesive, corporate-friendly experience sections.",
        "tags": ["Freelance", "Consulting", "Work History"],
        "prompt": "Translate my freelance or contract project experience into a single cohesive job description entry that reads like a professional consulting role. Focus on client satisfaction, scoping, deliverable quality, and business outcome. Raw Projects: [PROJECT_DETAILS] and Target Role: [TARGET_ROLE].",
        "exampleInput": "PROJECT_DETAILS: Built 3 different websites for local small shops. Did SEO optimization on them. Made them mobile friendly. Used Shopify and WordPress.\nTARGET_ROLE: Web Operations Manager",
        "exampleOutput": "Independent Web Consultant | 2024 - Present\n• Directed end-to-end web deployment projects for multiple SMB clients, delivering responsive e-commerce and CMS architectures.\n• Implemented search engine optimization (SEO) best practices, achieving an average 25% increase in organic search traffic within 90 days of launch.\n• Scoped technical requirements, negotiated service level agreements, and delivered on-budget integrations using Shopify and WordPress.",
        "tips": ["Use a unified title like 'Independent Consultant' or 'Lead Web Developer (Contractor)'.", "Highlight client management and scoping."]
    },
    {
        "id": "res-007",
        "title": "Action-Verbs & Variety Injector",
        "category": "resume",
        "difficulty": "Beginner",
        "description": "Replaces repetitive action verbs (like 'led', 'managed', 'worked') with a diverse and impactful vocabulary.",
        "tags": ["Vocabulary", "Editing", "Polishing"],
        "prompt": "Identify repetitive verbs in the following resume text and suggest dynamic, descriptive synonyms that align with the specific job function. Rewrite the text using these new verbs to create a more engaging read. Resume text: [RESUME_TEXT] and Job Function: [JOB_FUNCTION].",
        "exampleInput": "RESUME_TEXT: Led the sales team. Led client meetings. Managed new accounts. Worked with marketing to get leads. Managed CRM database.\nJOB_FUNCTION: Sales Director",
        "exampleOutput": "• Energized and directed a high-performing sales team.\n• Facilitated high-stakes client negotiations and presentations.\n• Acquired and cultivated strategic accounts to drive revenue growth.\n• Partnered with marketing to engineer lead acquisition funnels.\n• Maintained and optimized the CRM database to ensure pipeline accuracy.",
        "tips": ["Never use the same action verb more than twice on a single page.", "Select verbs that suggest specific soft or hard skills."]
    },
    {
        "id": "res-008",
        "title": "Resume Gap Explainer",
        "category": "resume",
        "difficulty": "Intermediate",
        "description": "Constructs brief, positive bullet points for resume gaps, detailing self-study, caregiving, or sabbatical learnings.",
        "tags": ["Resume Gap", "Career Break", "Framing"],
        "prompt": "Draft a professional explanation or bullet points for a career gap in my resume. Highlight self-directed learning, professional development, personal growth, or consulting work during this period, framing it as a strategic asset. Context of Gap: [GAP_CONTEXT] and Skills Acquired/Activities: [ACTIVITIES].",
        "exampleInput": "GAP_CONTEXT: Took 18 months off after a layoff to take care of a family member and complete a coding bootcamp.\nACTIVITIES: Completed a Full-Stack Javascript Bootcamp, built 3 full-stack React/Node projects, learned AWS basics.",
        "exampleOutput": "Professional Development & Specialized Training | 2024 - 2025\n• Dedicated 18-month career sabbatical to advanced technical upskilling, graduating from an intensive 800-hour Software Engineering Academy.\n• Designed, built, and deployed 3 full-stack web applications utilizing React, Node.js, and PostgreSQL to showcase modern engineering principles.\n• Attained cloud computing fundamentals through self-directed AWS training, focusing on serverless deployments and storage architectures.",
        "tips": ["Keep the tone confident and direct.", "Focus on the skills gained that make you ready for the next job."]
    },
    {
        "id": "res-009",
        "title": "Resume Layout Structure Audit",
        "category": "resume",
        "difficulty": "Beginner",
        "description": "Reviews the visual structure and section order of a resume based on years of experience and target seniority.",
        "tags": ["Formatting", "Structure", "Audit"],
        "prompt": "Analyze my resume sections, structure, and ordering. Provide recommendations on how to arrange them (e.g., Skills first, Education first, or Work Experience first) based on my years of experience and industry expectations. Details: [RESUME_OVERVIEW] and Years of Experience: [EXPERIENCE_YEARS].",
        "exampleInput": "RESUME_OVERVIEW: Education (BS in CS, graduated 2020), Skills (Python, Java), Projects (3 school projects), Work Experience (1 year junior dev, 4 years retail manager).\nEXPERIENCE_YEARS: 5 years total, 1 year in tech, 4 years prior retail.",
        "exampleOutput": "Suggested Layout Order:\n1. Contact Information & Headline (Clear target role)\n2. Professional Summary (Mention tech focus and transferable retail management leadership)\n3. Core Technical Skills (Grouped by language/tools)\n4. Professional Experience (Present tech role first; condense retail to highlight leadership/operations)\n5. Key Projects (Highlight full-stack projects to compensate for shorter formal tech tenure)\n6. Education (Move to bottom since you have been in the workforce for 5 years)",
        "tips": ["Always put the most relevant experience on the top half of the first page.", "Once you have 2+ years of experience, move Education to the bottom."]
    },
    {
        "id": "res-010",
        "title": "Achievement Extractor",
        "category": "resume",
        "difficulty": "Intermediate",
        "description": "Asks clarifying questions or prompts to help you extract measurable achievements from a daily task list.",
        "tags": ["Metrics", "Achievements", "Interview Preparation"],
        "prompt": "Convert a list of mundane daily responsibilities into bullet points that emphasize accomplishments, achievements, and impact. Help me identify the hidden metrics. Responsibilities list: [RESPONSIBILITIES] and Industry/Domain: [DOMAIN].",
        "exampleInput": "RESPONSIBILITIES: Answered customer support tickets, dealt with complaints, updated help center articles.\nDOMAIN: Customer Success",
        "exampleOutput": "• Resolved an average of 45+ customer support inquiries daily, maintaining a 97% Customer Satisfaction (CSAT) score.\n• Spearheaded the overhaul of the external Knowledge Base, authoring 30+ help articles that decreased inbound ticket volume by 15%.\n• Analyzed customer complaint trends, collaborating with the product team to fix 5 repeating software issues.",
        "tips": ["Think about: How many? How fast? How much money? Who benefited? How did you stand out?"]
    }
]
prompts.extend(res_data)

# --- 2. ATS PROMPTS (id: ats-001 to ats-010) ---
ats_data = [
    {
        "id": "ats-001",
        "title": "Job Description Keyword Extractor",
        "category": "ats",
        "difficulty": "Beginner",
        "description": "Extracts the exact hard skills, certifications, and soft skills from a job description for ATS optimization.",
        "tags": ["Keywords", "Job Description", "ATS Audit"],
        "prompt": "Analyze the following job description and extract: 1. Core Hard Skills (must-haves). 2. Preferred / Nice-to-have Skills. 3. Essential Soft Skills / Competencies. 4. Important industry acronyms and tool names. Job Description: [JOB_DESCRIPTION].",
        "exampleInput": "JOB_DESCRIPTION: We are seeking a Senior Product Manager. Must have 5+ years experience, solid understanding of Agile/Scrum, JIRA, and SQL. Experience with Mixpanel or Amplitude is a big plus. Excellent communication and stake-holder alignment skills are needed. Certified Product Owner (CSPO) preferred.",
        "exampleOutput": "1. Core Hard Skills: Product Management (5+ years), Agile/Scrum, JIRA, SQL\n2. Preferred/Nice-to-have: Mixpanel, Amplitude, Certified Product Owner (CSPO)\n3. Essential Soft Skills: Communication, Stakeholder Alignment\n4. Acronyms & Tools: JIRA, SQL, CSPO, Mixpanel, Amplitude, PM",
        "tips": ["Incorporate these exact terms in your resume exactly as they are written in the description."]
    },
    {
        "id": "ats-002",
        "title": "ATS Synonym Matcher",
        "category": "ats",
        "difficulty": "Intermediate",
        "description": "Reviews a resume for acronym variations and lists standardized terms that ATS search parsers easily recognize.",
        "tags": ["Synonyms", "Formatting", "Acronyms"],
        "prompt": "For the following skills and certifications, provide both the abbreviated version and the fully spelled-out version to ensure the ATS parser picks them up regardless of search query style. Skills list: [SKILLS_LIST].",
        "exampleInput": "SKILLS_LIST: AWS, CSPO, MBA, KPI, SEO, NLP, CI/CD",
        "exampleOutput": "• AWS -> Amazon Web Services (AWS)\n• CSPO -> Certified Scrum Product Owner (CSPO)\n• MBA -> Master of Business Administration (MBA)\n• KPI -> Key Performance Indicators (KPIs)\n• SEO -> Search Engine Optimization (SEO)\n• NLP -> Natural Language Processing (NLP)\n• CI/CD -> Continuous Integration / Continuous Deployment (CI/CD)",
        "tips": ["Always spell out an acronym on its first occurrence on your resume, followed by the abbreviation in parentheses."]
    },
    {
        "id": "ats-003",
        "title": "Resume vs Job Description Gap Analyst",
        "category": "ats",
        "difficulty": "Advanced",
        "description": "Compares your resume text against a job description to flag missing keywords, mismatching titles, and structural gaps.",
        "tags": ["Gap Analysis", "Resume Audit", "Optimization"],
        "prompt": "Act as an ATS parser. Compare my resume against the job description below. Identify: 1. Critical keywords missing from my resume. 2. Experience or requirement gaps. 3. Suggestions on where and how to integrate the missing keywords based on my background. Resume: [YOUR_RESUME] Job Description: [JOB_DESCRIPTION].",
        "exampleInput": "YOUR_RESUME: Software engineer with 3 years experience. Stack: React, node.js, mongoDB. Built web apps, worked in agile teams.\nJOB_DESCRIPTION: Senior Full Stack Engineer. Requires 5+ years experience, AWS cloud deployments, TypeScript, CI/CD pipelines, and PostgreSQL database optimization.",
        "exampleOutput": "1. Critical Keywords Missing: TypeScript, AWS, CI/CD, PostgreSQL, 5+ years experience\n2. Gaps: Tenure gap (3 years vs 5 required), lack of cloud infrastructure (AWS) and relational database (PostgreSQL) experience.\n3. Integration Strategy: If you have used TypeScript or worked on AWS/CI/CD in personal projects, create a dedicated 'Projects' section and list them. If you have used SQL or PostgreSQL in past roles, rephrase 'mongoDB' bullets to highlight relational database experience.",
        "tips": ["Do not copy-paste text you didn't do; instead, re-frame adjacent work to cover the keywords honestly."]
    },
    {
        "id": "ats-004",
        "title": "ATS-Friendly Layout & Formatting Auditor",
        "category": "ats",
        "difficulty": "Beginner",
        "description": "Reviews the layout items (tables, text boxes, columns) and alerts you on elements that typically break ATS parsers.",
        "tags": ["Formatting", "ATS friendly", "Structure"],
        "prompt": "Evaluate my planned resume formatting choices. Flag any items that are known to cause parsing errors in major Applicant Tracking Systems (e.g., Workday, Taleo, Greenhouse) and suggest safer alternatives. Formatting Choices: [FORMATTING_CHOICES].",
        "exampleInput": "FORMATTING_CHOICES: Double-column layout, profile picture in top left, skill bars showing 80% proficiency, custom icons for email/phone, tables for project details, saved as PDF.",
        "exampleOutput": "• DOUBLE-COLUMN LAYOUT: High risk. Parsers read left-to-right across columns, jumbling text. Change to Single-Column.\n• PROFILE PICTURE: High risk. Parsers might reject the resume entirely due to compliance/bias protocols. Remove photo.\n• SKILL BARS: High risk. Graphic bars are unreadable. Change to written text.\n• TABLES: High risk. Parsers often skip text in tables. Remove tables and use standard tabs.",
        "tips": ["Stick to simple, standard fonts like Arial, Calibri, or Times New Roman.", "A standard PDF or DOCX is ideal."]
    },
    {
        "id": "ats-005",
        "title": "Targeted Headline Customizer",
        "category": "ats",
        "difficulty": "Intermediate",
        "description": "Aligns your current job title and subheading with the specific title in the target job posting.",
        "tags": ["Job Title", "Headline", "Relevance"],
        "prompt": "Help me customize my resume headline and target job title. My current title is [CURRENT_TITLE] and the job I want to apply for is [TARGET_JOB_TITLE]. Give me 3 options for the top header of my resume that bridge this gap while staying truthful. Here is my experience overview: [EXPERIENCE_SUMMARY].",
        "exampleInput": "CURRENT_TITLE: Quality Assurance Specialist\nTARGET_JOB_TITLE: Senior QA Automation Engineer\nEXPERIENCE_SUMMARY: 6 years total, developed Selenium and Cypress test frameworks, led automation strategies.",
        "exampleOutput": "Option 1: Senior QA Automation Engineer (Direct match)\nOption 2: QA Engineer | Automation & Cypress Specialist\nOption 3: Senior Quality Assurance Engineer (Test Automation & Selenium Developer)",
        "tips": ["Always match the primary target title as closely as possible without exaggerating your experience level."]
    },
    {
        "id": "ats-006",
        "title": "Job-to-Resume Bullet Point Customizer",
        "category": "ats",
        "difficulty": "Advanced",
        "description": "Takes a specific bullet point from a job description and tailovers your existing resume bullets to address it directly.",
        "tags": ["Bullet Points", "Job Description", "Tailoring"],
        "prompt": "Take my resume bullet point and customize it to align directly with a specific requirement from the job description, using their terminology while keeping my core metrics intact. Current Resume Bullet: [YOUR_BULLET] Job Requirement: [JOB_REQUIREMENT].",
        "exampleInput": "YOUR_BULLET: Created a dashboard that showed team productivity and sped up project deliveries by 10%.\nJOB_REQUIREMENT: Build internal monitoring tools and dashboards using React and Redux to track key operations metrics.",
        "exampleOutput": "Designed and deployed internal operation dashboards using React and Redux, tracking key performance metrics to accelerate team delivery times by 10%.",
        "tips": ["Use the same verbs and technical terms as the job posting."]
    },
    {
        "id": "ats-007",
        "title": "Standard Section Header Auditor",
        "category": "ats",
        "difficulty": "Beginner",
        "description": "Replaces creative or fancy section titles with standard, ATS-parseable headings.",
        "tags": ["Section Headers", "Formatting", "Standardization"],
        "prompt": "Check my resume's section headers. If they are too creative, suggest standard alternatives that ATS parsers will recognize and categorize properly. My current headers: [CURRENT_HEADERS].",
        "exampleInput": "CURRENT_HEADERS: Who I Am, Where I've Been, Professional Odyssey, Tools of the Trade, Accolades, Knowledge.",
        "exampleOutput": "• Who I Am -> Professional Summary\n• Where I've Been / Professional Odyssey -> Professional Experience\n• Tools of the Trade / Knowledge -> Core Skills\n• Accolades -> Awards & Achievements",
        "tips": ["Don't try to stand out with section names; stand out with your achievements. Keep names standard."]
    },
    {
        "id": "ats-008",
        "title": "ATS Date Formatting Assistant",
        "category": "ats",
        "difficulty": "Beginner",
        "description": "Converts date formats into clean, standardized systems that parsers read correctly to calculate tenure.",
        "tags": ["Dates", "Tenure", "Formatting"],
        "prompt": "Convert my miscellaneous date formats into standard resume formats (MM/YYYY or Month YYYY) so the ATS can accurately calculate my tenure in each role. Dates list: [DATES_LIST].",
        "exampleInput": "DATES_LIST: June '18 - Dec '20, 2021-2023, Fall 2023 to Present, 08/20 - 05/21",
        "exampleOutput": "• June '18 - Dec '20 -> 06/2018 - 12/2020 (or June 2018 - December 2020)\n• 2021-2023 -> 01/2021 - 12/2023 (Spell out months for better accuracy)\n• Fall 2023 to Present -> 09/2023 - Present\n• 08/20 - 05/21 -> 08/2020 - 05/2021",
        "tips": ["Never use seasons (e.g. 'Fall' or 'Summer') as dates; ATS parsers cannot reliably convert them."]
    },
    {
        "id": "ats-009",
        "title": "Keyword Density Checker",
        "category": "ats",
        "difficulty": "Intermediate",
        "description": "Reviews the frequency of target keywords on your resume to prevent artificial stuffing while maintaining professional relevance.",
        "tags": ["Keyword Density", "Word Count", "Optimization"],
        "prompt": "Act as an ATS auditor. Analyze this resume text for a target keyword [KEYWORD]. Check how many times it appears, and tell me if the density is natural (1-3%) or if it looks stuffed. Provide rewrite advice. Resume text: [RESUME_TEXT].",
        "exampleInput": "KEYWORD: Project Manager\nRESUME_TEXT: Project Manager with 5 years experience as a project manager. As a project manager, I did project manager duties for project manager teams.",
        "exampleOutput": "Keyword 'Project Manager' density is 10%, which is extremely high and flags as keyword stuffing. Suggest rewriting to include synonyms like 'Project Leader', 'Program Manager', or focusing on action verbs like 'orchestrated development pipelines'.",
        "tips": ["Integrate keywords in context rather than repeating them in an unnatural list."]
    },
    {
        "id": "ats-010",
        "title": "ATS Contact Info Formatter",
        "category": "ats",
        "difficulty": "Beginner",
        "description": "Formats headers to ensure the ATS extracts phone numbers, emails, and LinkedIn links without losing them in text boxes.",
        "tags": ["Contact Details", "Formatting", "Header"],
        "prompt": "Format my contact details into a single clean line suitable for an ATS header. Ensure it does not contain tables, headers/footers (where text gets lost in some systems), or text boxes. Contact details: [CONTACT_DETAILS].",
        "exampleInput": "CONTACT_DETAILS: Name: John Doe, Email: john.doe@email.com, Phone: 123-456-7890, Address: Austin TX, LinkedIn: linkedin.com/in/johndoe",
        "exampleOutput": "John Doe | Austin, TX | 123-456-7890 | john.doe@email.com | linkedin.com/in/johndoe",
        "tips": ["Do not place contact information in the document header or footer section, as many older ATS parsers ignore these sections entirely."]
    }
]
prompts.extend(ats_data)

# --- 3. COVER LETTER PROMPTS (id: cov-001 to cov-010) ---
cov_data = [
    {
        "id": "cov-001",
        "title": "The Hook Generator",
        "category": "cover-letter",
        "difficulty": "Beginner",
        "description": "Generates a strong, attention-grabbing opening paragraph for a cover letter, avoiding cliché openings.",
        "tags": ["Hook", "Introduction", "Opening Paragraph"],
        "prompt": "Generate 3 different options for the opening paragraph of my cover letter. Avoid clichés like 'I am writing to express my interest'. Option 1: Passion-driven. Option 2: Metrics-driven (starting with a big achievement). Option 3: Connection-driven (citing a company value, article, or mutual contact). Here is my info: [YOUR_INFO] and the company/role: [COMPANY_ROLE].",
        "exampleInput": "YOUR_INFO: 4 years experience as software developer, increased app load speed by 50%.\nCOMPANY_ROLE: Stripe / Frontend Engineer.",
        "exampleOutput": "Option 1 (Passion-driven): As a developer who values clean APIs and developer-first experiences, I have long admired Stripe's commitment to building frictionless financial infrastructure. \nOption 2 (Metrics-driven): When I optimized database query response times by 50% in my previous role, I realized the power of micro-optimizations. I want to bring that same focus on performance to Stripe.\nOption 3 (Connection-driven): I recently read your blog post on building API-driven interfaces, and it resonated deeply with my experience refactoring frontend systems.",
        "tips": ["Keep the opening to 3 sentences maximum.", "State the target role clearly but creatively."]
    },
    {
        "id": "cov-002",
        "title": "Company Pain-Point Matcher",
        "category": "cover-letter",
        "difficulty": "Advanced",
        "description": "Aligns your past experiences directly with a major challenge or initiative the company is currently facing.",
        "tags": ["Pain Point", "Value Proposition", "Problem Solving"],
        "prompt": "Draft the middle paragraph of my cover letter. Frame it around a challenge the target company is facing, showing how my background directly prepares me to solve it. Company pain point: [PAIN_POINT], my relevant experience: [MY_EXPERIENCE].",
        "exampleInput": "PAIN_POINT: The company is scaling their engineering team quickly and struggling with developer onboarding latency.\nMY_EXPERIENCE: I created an onboarding wiki and mentorship program at my last company, reducing developer setup times from 2 weeks to 3 days.",
        "exampleOutput": "I understand that as your team enters a phase of rapid scaling, onboarding developer talent quickly is top of mind. In my previous role, I addressed this bottleneck by designing a comprehensive developer onboarding portal and establishing a peer-mentorship program. This initiative reduced environment setup latency from 14 days to just 3 days, accelerating product delivery speeds for new hires.",
        "tips": ["Identify the pain point through job postings, articles, or networking conversations.", "Show, don't tell."]
    },
    {
        "id": "cov-003",
        "title": "Storytelling-style Cover Letter Builder",
        "category": "cover-letter",
        "difficulty": "Intermediate",
        "description": "Drafts a cover letter structured around a single compelling narrative of a professional challenge you solved.",
        "tags": ["Storytelling", "STAR Method", "Narrative"],
        "prompt": "Create a cover letter draft centered around a professional story. Use a narrative arc: 1. The challenge/crisis. 2. The strategy I implemented. 3. The business impact. 4. How this applies to the target company. Role details: [ROLE], Story context: [STORY_CONTEXT].",
        "exampleInput": "ROLE: Marketing Director\nSTORY_CONTEXT: At my last job, traffic dropped by 30% due to a Google algorithm update. I led a content audit, redirected dead links, and recovered traffic within 4 months, plus got an extra 15% increase.",
        "exampleOutput": "Dear Hiring Manager,\n\nWhen our organic traffic plummeted by 30% overnight due to a core algorithm update, my team faced a critical choice. As Marketing Director, I immediately orchestrated a site-wide content audit, refactoring 150 legacy pages and redirecting orphaned URLs. Within four months, we not only recovered our baseline traffic but recorded an additional 15% growth in organic acquisitions. I hope to bring this proactive problem-solving to your team.",
        "tips": ["Make sure the story highlights collaboration and resourcefulness.", "Keep the narrative concise."]
    },
    {
        "id": "cov-004",
        "title": "Bullet-Points Cover Letter Writer",
        "category": "cover-letter",
        "difficulty": "Beginner",
        "description": "Writes a modern, skimmable cover letter that uses structured bullet points instead of dense paragraphs.",
        "tags": ["Skimmable", "Bullet Points", "Modern Layout"],
        "prompt": "Generate a cover letter that uses clean bullet points in the middle section to call out 3 key achievements that match the job description. Make it highly skimmable for busy recruiters. Achievements: [ACHIEVEMENTS] Job Description: [JOB_DESC].",
        "exampleInput": "ACHIEVEMENTS: Managed $1M budget, saved 10% costs, hired 5 people.\nJOB_DESC: Operational Manager needing budget oversight and team-building experience.",
        "exampleOutput": "Dear Hiring Team,\n\nI am thrilled to apply for the Operations Manager position. Over the past five years, I have developed a track record of driving operational efficiency. Here are three key achievements that align with your team's current goals:\n\n• Budget Oversight: Managed a $1M operational budget, successfully reducing waste to save 10% in annual overhead.\n• Team Building: Recruited and trained 5 cross-functional professionals, maintaining a 100% retention rate.\n• Process Improvement: Implemented digital workflows that accelerated project approvals.",
        "tips": ["Limit bullet points to exactly three.", "Use bold lead-ins for each bullet."]
    },
    {
        "id": "cov-005",
        "title": "Referral-Mention Cover Letter",
        "category": "cover-letter",
        "difficulty": "Intermediate",
        "description": "Integrates a warm introduction or referral from an employee at the target company naturally into the letter.",
        "tags": ["Referral", "Networking", "Introduction"],
        "prompt": "Draft a cover letter opening that naturally mentions a referral from a current employee at the company. Specify the context of our professional relationship and why they suggested I apply. Referrer Name: [REFERRER], Context: [REFERRER_CONTEXT], Role & Company: [ROLE_COMPANY].",
        "exampleInput": "REFERRER: Sarah Jenkins (Lead Product Designer)\nREFERRER_CONTEXT: Met at an UX conference, she reviewed my portfolio and said my design approach fits their product team.\nROLE_COMPANY: UX Researcher at Figma.",
        "exampleOutput": "Dear Hiring Manager,\n\nFollowing a conversation with Sarah Jenkins, Lead Product Designer at Figma, she suggested I reach out regarding the UX Researcher opening. Sarah and I connected at the annual UX Design Conference, where we discussed Figma's research methodology. Based on my background in cognitive research, she believed my approach to user testing would integrate seamlessly with your current product roadmap.",
        "tips": ["Ensure you have the referrer's explicit permission to mention them.", "Put their name in the first paragraph."]
    },
    {
        "id": "cov-006",
        "title": "Short Email-body Cover Letter",
        "category": "cover-letter",
        "difficulty": "Beginner",
        "description": "Writes a condensed cover letter (under 150 words) suitable for the body of an email when attaching a resume.",
        "tags": ["Email", "Short Form", "Direct Outreach"],
        "prompt": "Write a short, professional cover letter to be used as the body of an email. Keep it under 150 words, focusing on my top selling point, my attached resume, and a clear call to action. Details: [DETAILS].",
        "exampleInput": "DETAILS: Customer Success Manager, 3 years experience, 95% CSAT score, applying to Acme Corp.",
        "exampleOutput": "Subject: Customer Success Manager Application - [My Name]\n\nDear Acme Corp Hiring Team,\n\nI am writing to express my enthusiastic interest in the Customer Success Manager position. As a CS professional with 3 years of experience, I specialize in building long-term client relationships and optimizing renewal pipelines. \n\nAt my previous company, I maintained a consistent 95% CSAT score while reducing client onboarding latency. I have attached my resume, which details these achievements.\n\nI welcome the opportunity to discuss how my customer-centric approach can add value to your team. Thank you for your time.\n\nBest regards,\n\n[My Name]\n[My Phone Number]",
        "tips": ["Ensure the subject line is clear and professional.", "Use simple formatting."]
    },
    {
        "id": "cov-007",
        "title": "Creative / Culture-Fit Cover Letter",
        "category": "cover-letter",
        "difficulty": "Intermediate",
        "description": "Writes a cover letter for startup or creative roles, emphasizing cultural alignment, mission passion, and personality.",
        "tags": ["Creative", "Startup", "Culture Fit"],
        "prompt": "Create a cover letter for a creative or startup environment. The tone should be enthusiastic, conversational, yet professional. Highlight alignment with their mission and values. Mission: [MISSION], Target Role: [ROLE], My background: [BACKGROUND].",
        "exampleInput": "MISSION: Democreatize design tools so anyone can create.\nROLE: Content Strategist at Canva.\nBACKGROUND: Run a popular design tutorial blog, self-taught designer, love teaching others.",
        "exampleOutput": "Dear Canva Team,\n\nI've spent the last three years building a digital community around self-taught design, and if there's one thing I've learned, it's that access changes everything. When design tools are democratized, communities thrive. This is why Canva's mission resonates with me on a personal level. As a self-taught creator, I want to bring my passion for teaching design to Canva as a Content Strategist.",
        "tips": ["Do not sound overly stiff or corporate.", "Use the company's core values as hooks."]
    },
    {
        "id": "cov-008",
        "title": "Follow-Up Cover Letter (Late Application)",
        "category": "cover-letter",
        "difficulty": "Beginner",
        "description": "Addresses cases where you are submitting an application late or following up after an initial window.",
        "tags": ["Follow-Up", "Late Submission", "Polite"],
        "prompt": "Write a cover letter designed for a follow-up or late submission. Express enthusiasm, address the delay briefly without sounding apologetic, and emphasize how you can immediately hit the ground running. Role: [ROLE], Context: [CONTEXT].",
        "exampleInput": "ROLE: Sales Executive\nCONTEXT: The job was posted 3 weeks ago, I was finishing a major project, I have a warm lead list ready.",
        "exampleOutput": "Dear Hiring Manager,\n\nWhile I understand your search for a Sales Executive is well underway, I wanted to submit my application as I believe my profile aligns perfectly with your growth goals. I have spent the last month successfully delivering a major sales campaign. I am eager to bring my active pipeline of warm enterprise contacts to your team and hit the ground running.",
        "tips": ["Keep it forward-looking.", "Emphasize immediate productivity."]
    },
    {
        "id": "cov-009",
        "title": "The Call-to-Action Closing Paragraph",
        "category": "cover-letter",
        "difficulty": "Beginner",
        "description": "Drafts strong concluding lines that state your availability and invite a conversation, avoiding passive endings.",
        "tags": ["Closing", "Call to Action", "Conclusion"],
        "prompt": "Generate 3 alternative closing paragraphs for a cover letter. Each option should create a natural call to action (interview invitation) without sounding presumptuous or desperate. My Availability/Details: [DETAILS].",
        "exampleInput": "DETAILS: Ready to start immediately, located in Chicago, open to hybrid/remote.",
        "exampleOutput": "Option 1: I welcome the opportunity to discuss my qualifications in an interview. I am based in Chicago and available for a call or meeting at your earliest convenience.\nOption 2: Thank you for your time and consideration. I look forward to exploring how my background aligns with your team's objectives during a conversation.\nOption 3: I am eager to share more details about my past projects. I am available for an interview and can be reached via phone or email.",
        "tips": ["Avoid saying 'I will call your office next week'. Keep the ball in their court but open."]
    },
    {
        "id": "cov-010",
        "title": "Resume Gap Re-framer (Cover Letter)",
        "category": "cover-letter",
        "difficulty": "Intermediate",
        "description": "Explains a significant career break in a positive light within the body of a cover letter.",
        "tags": ["Career Break", "Reframing", "Cover Letter Body"],
        "prompt": "Draft a paragraph for my cover letter that addresses a gap in my work history in a positive, professional manner. Focus on what was gained and how it prepares me for this role. Gap Reason: [REASON], Target Role: [ROLE].",
        "exampleInput": "REASON: Took 2 years off to travel and do volunteer project management abroad.\nROLE: Project Manager.",
        "exampleOutput": "During a two-year professional sabbatical, I volunteered as a Project Manager for community development initiatives abroad. Leading cross-cultural teams under resource constraints sharpened my risk management and negotiation skills. I am excited to bring this global perspective back to my career as a full-time Project Manager.",
        "tips": ["Limit the explanation to 2-3 sentences.", "Pivot back to the role requirements quickly."]
    }
]
prompts.extend(cov_data)

# --- 4. INTERVIEW PROMPTS (id: int-001 to int-010) ---
int_data = [
    {
        "id": "int-001",
        "title": "STAR Method Response Planner",
        "category": "interview",
        "difficulty": "Intermediate",
        "description": "Structures raw stories into structured Situation, Task, Action, and Result (STAR) formats for behavioral questions.",
        "tags": ["STAR Method", "Behavioral", "Prep"],
        "prompt": "Take my raw experience story and structure it using the STAR method (Situation, Task, Action, Result) for an interview. Make it concise, professional, and highlight the metrics. Raw Story: [RAW_STORY] Target Question: [TARGET_QUESTION].",
        "exampleInput": "RAW_STORY: We had a customer complain about data loss. I stayed up late, found the bug, fixed it, and updated the backup script. The customer was happy and renewed.\nTARGET_QUESTION: Tell me about a time you handled a high-pressure situation.",
        "exampleOutput": "• Situation: A tier-one customer reported critical data loss due to a sync issue during peak hours, threatening their contract renewal.\n• Task: I was tasked with identifying the bug immediately and restoring service without further data corruption.\n• Action: I triaged the log files, isolated the sync bug in the database layer, deployed a hotfix within 3 hours, and rewrote the backup scripts.\n• Result: Restored 100% of the customer's data. The client renewed their annual contract, resulting in a $50k retention.",
        "tips": ["The 'Action' should represent 50% of the response.", "Make sure the 'Result' contains a business metric."]
    },
    {
        "id": "int-002",
        "title": "Technical Case Study Mock",
        "category": "interview",
        "difficulty": "Advanced",
        "description": "Generates simulated case studies for system design, product strategy, or consulting interviews.",
        "tags": ["Case Study", "System Design", "Mock Interview"],
        "prompt": "Generate a technical case study scenario for a [ROLE] interview at a [COMPANY_TYPE] company. Include: 1. The core challenge. 2. 3 clarifying questions I should ask. 3. A structured framework for presenting the solution.",
        "exampleInput": "ROLE: Systems Architect\nCOMPANY_TYPE: E-Commerce scale-up (Black Friday traffic spike prep)",
        "exampleOutput": "1. Challenge: Design a checkout system that handles a 10x traffic spike during flash sales.\n2. Clarifying Questions to Ask:\n   - What is the target write latency during peaks?\n   - Are we prioritizing consistency or availability?\n   - Can we offer asynchronous order processing?\n3. Framework: \n   - Identify bottlenecks (Database, Payment Gateways).\n   - Propose Queueing (RabbitMQ/Kafka).\n   - Implement Caching (Redis).\n   - Design Database Scaling (Read Replicas, Sharding).",
        "tips": ["Always ask clarifying questions before jumping into a solution during the actual interview."]
    },
    {
        "id": "int-003",
        "title": "Reverse Question Generator",
        "category": "interview",
        "difficulty": "Beginner",
        "description": "Creates questions to ask the interviewer about culture, technology, and expectations to stand out.",
        "tags": ["Questions to Ask", "End of Interview", "Culture"],
        "prompt": "Generate 5 thoughtful questions to ask my interviewer at the end of the interview. Make them specific to the role of [ROLE] and the company culture/challenges. Target Company Details: [COMPANY_DETAILS].",
        "exampleInput": "ROLE: Senior Data Analyst\nCOMPANY_DETAILS: Healthcare SaaS, scaling data engineering team, trying to build automated reporting.",
        "exampleOutput": "1. What does a successful first 90 days look like for the Senior Data Analyst?\n2. With the data engineering team scaling, how do you balance maintaining data quality with the speed of new analytics requests?\n3. How do you protect patient data privacy during analysis?\n4. What is the biggest roadblock the team faces when building automated reporting?\n5. What is the team's approach to technical debt?",
        "tips": ["Avoid asking questions that can be easily answered by a Google search.", "Focus on challenges the team faces."]
    },
    {
        "id": "int-004",
        "title": "'Tell Me About Yourself' Writer",
        "category": "interview",
        "difficulty": "Beginner",
        "description": "Drafts a polished 90-second elevator pitch that introduces your background, achievements, and fit.",
        "tags": ["Elevator Pitch", "Self Introduction", "First Impression"],
        "prompt": "Write a 90-second script for the 'Tell me about yourself' interview question. Structure it around: Present (current role & focus), Past (key career highlights), and Future (why this target role is the logical next step). Background: [BACKGROUND] Target Role: [ROLE].",
        "exampleInput": "BACKGROUND: Currently a QA analyst. Used to do customer support. Want to transition to Product Owner.\nROLE: Junior Product Owner.",
        "exampleOutput": "Present: Currently, I am a QA Analyst at Acme Corp, where I specialize in user acceptance testing and translating user feedback into technical requirements.\nPast: Before QA, I spent two years in Customer Support. That experience gave me a deep understanding of user pain points and the impact of product decisions.\nFuture: I am looking to transition into product ownership, where I can leverage my QA and support background to define product requirements.",
        "tips": ["Keep it under 2 minutes.", "Keep it professional; don't mention hobbies unless relevant."]
    },
    {
        "id": "int-005",
        "title": "Weakness & Failure Frame Planner",
        "category": "interview",
        "difficulty": "Intermediate",
        "description": "Frames your weaknesses or past project failures as positive learning experiences.",
        "tags": ["Weakness", "Failure", "Reframing"],
        "prompt": "Draft a response to the question: 'What is your biggest weakness?' or 'Tell me about a time you failed.' Frame it so the weakness is a genuine area of improvement, and detail the active steps I have taken to overcome it. My Weakness/Failure: [WEAKNESS_FAILURE].",
        "exampleInput": "WEAKNESS_FAILURE: I have a hard time delegating tasks. I try to do everything myself because I think I can do it faster.",
        "exampleOutput": "My biggest weakness has been a tendency to take on too much myself rather than delegating. I used to think doing tasks myself was faster. However, I realized this creates a bottleneck. To address this, I started using project management tools to assign tasks clearly and set up checkpoint meetings to trust my team.",
        "tips": ["Never suggest a fake weakness like 'I work too hard'.", "Focus on what you learned."]
    },
    {
        "id": "int-006",
        "title": "Architectural Deep-Dive Preparer",
        "category": "interview",
        "difficulty": "Advanced",
        "description": "Prepares you to explain complex technical architectures or designs you built in past roles.",
        "tags": ["Architecture", "System Design", "Technical Interview"],
        "prompt": "Prepare an outline to explain a complex project I built. Structure the explanation for a technical interviewer: 1. High-level architecture. 2. Trade-offs made. 3. Bottlenecks identified. 4. Scale metrics. Project details: [PROJECT_DETAILS].",
        "exampleInput": "PROJECT_DETAILS: Built a microservices-based notification system using Node.js, Redis, and AWS SNS/SQS to handle 1M daily notifications.",
        "exampleOutput": "1. High-Level Architecture: Client -> API Gateway -> Express Service -> SQS -> Worker Service -> SNS -> Recipient.\n2. Trade-Offs: Chose asynchronous processing over synchronous delivery to handle traffic spikes, accepting slight delivery latency.\n3. Bottlenecks: Solved SQS polling cost bottlenecks by implementing long-polling.\n4. Scale Metrics: Handled 1M daily notifications with 99.9% uptime.",
        "tips": ["Draw a diagram if possible.", "Focus on the trade-offs; interviewers love to hear why you chose one tool over another."]
    },
    {
        "id": "int-007",
        "title": "Soft-Skills Response Tuner",
        "category": "interview",
        "difficulty": "Beginner",
        "description": "Polishes answers to focus on collaboration, conflict resolution, and teamwork.",
        "tags": ["Soft Skills", "Collaboration", "Conflict Resolution"],
        "prompt": "Tune my draft response to a soft-skills question. Make it sound more collaborative and professional. Draft: [DRAFT_RESPONSE] Target Question: [QUESTION].",
        "exampleInput": "DRAFT_RESPONSE: My coworker was not doing their work. I got mad, sat down with them, and told them they are slowing us down. They did better.\nQUESTION: How do you handle conflict with a teammate?",
        "exampleOutput": "When a teammate fell behind on deliverables, I scheduled a private check-in to understand if they were facing blockers. We mapped out task dependencies together, which helped resolve the workflow issues without escalating. This approach restored delivery timelines.",
        "tips": ["Avoid blaming coworkers.", "Show empathy and collaboration."]
    },
    {
        "id": "int-008",
        "title": "Pitch Presentation Preparation",
        "category": "interview",
        "difficulty": "Intermediate",
        "description": "Outlines a slide deck or talk for interviews that require a presentation or case study pitch.",
        "tags": ["Presentation", "Pitching", "Interview Prep"],
        "prompt": "Create an outline for a 10-minute presentation for my interview. Topic: [TOPIC] Target Audience: [AUDIENCE]. Include slide-by-slide topics and key talking points.",
        "exampleInput": "TOPIC: How to improve user retention for a fitness app.\nAUDIENCE: Product Leadership Team.",
        "exampleOutput": "Slide 1: Title & Introduction (The retention challenge)\nSlide 2: Executive Summary (The 3-point strategy)\nSlide 3: User Research & Pain Points (Why users churn after week 2)\nSlide 4: Solution 1: Personalized onboarding\nSlide 5: Solution 2: Gamification mechanics\nSlide 6: Solution 3: Re-engagement campaigns\nSlide 7: Metrics & ROI (Targeting 15% improvement)\nSlide 8: Q&A & Discussion",
        "tips": ["Keep slides visual.", "Focus on business value."]
    },
    {
        "id": "int-009",
        "title": "Post-Interview Feedback Request",
        "category": "interview",
        "difficulty": "Beginner",
        "description": "Drafts professional emails to request feedback after receiving a rejection.",
        "tags": ["Feedback", "Email", "Rejection"],
        "prompt": "Write a polite email asking for constructive feedback after being rejected for a role. Make it professional and focused on growth. Details: [DETAILS].",
        "exampleInput": "DETAILS: Interviewed for Front-End Engineer, made it to final round, rejected yesterday.",
        "exampleOutput": "Subject: Thank you - [My Name] - Front-End Engineer Application\n\nDear [Interviewer Name],\n\nThank you for letting me know about your decision regarding the Front-End Engineer position. While I am disappointed, I appreciate the opportunity to meet the team.\n\nAs I continue to develop my skills, I would appreciate any constructive feedback you could share about my final round interview. \n\nThank you again for your time.\n\nBest regards,\n[My Name]",
        "tips": ["Send the email within 48 hours of the rejection.", "Keep it brief and polite."]
    },
    {
        "id": "int-010",
        "title": "Tough Question Prep (Layoffs/Firings)",
        "category": "interview",
        "difficulty": "Intermediate",
        "description": "Prepares honest, professional explanations for why you left your last job under tough circumstances.",
        "tags": ["Layoffs", "Termination", "Difficult Questions"],
        "prompt": "Help me prepare an explanation for why I left my previous employer. Context: [CONTEXT]. Keep it concise, neutral, and forward-looking, avoiding any negative comments about the former employer.",
        "exampleInput": "CONTEXT: The company had a 30% layoff because of funding issues, my department was shut down.",
        "exampleOutput": "Due to a company restructuring and funding reallocation, my department was eliminated. I am proud of the work we accomplished and am looking forward to applying my skills in a more stable, growth-oriented environment.",
        "tips": ["Never complain about your former company.", "Keep the explanation brief."]
    }
]
prompts.extend(int_data)

# --- 5. LINKEDIN PROMPTS (id: lnk-001 to lnk-010) ---
lnk_data = [
    {
        "id": "lnk-001",
        "title": "LinkedIn Headline Optimizer",
        "category": "linkedin",
        "difficulty": "Beginner",
        "description": "Generates keyword-rich headlines that stand out in search results and feed rankings.",
        "tags": ["Headline", "Profile", "Keywords"],
        "prompt": "Generate 5 LinkedIn headlines based on my background. Format: [Title] | [Key Skill] | [Value Add/Metric]. Background details: [BACKGROUND] Target Role: [ROLE].",
        "exampleInput": "BACKGROUND: Full stack developer, React expert, optimized web apps, 4 years experience.\nROLE: Frontend Architect.",
        "exampleOutput": "1. Frontend Architect | React & TypeScript Expert | Scaling Performance by 40%\n2. Senior Frontend Engineer | Building Intuitive User Interfaces | UI/UX Specialist\n3. Web Architect | React, Node.js, Cloud Architectures | Reducing System Latency\n4. Frontend Architect | Technical Lead | Delivering Production-Grade Web Apps\n5. Senior Frontend Developer | Transforming User Experiences | Agile Lead",
        "tips": ["Use vertical bars (|) to separate sections.", "Include search keywords."]
    },
    {
        "id": "lnk-002",
        "title": "LinkedIn 'About' Section Storyteller",
        "category": "linkedin",
        "difficulty": "Intermediate",
        "description": "Drafts an engaging 'About' section that tells your professional story, core values, and specialties.",
        "tags": ["About Section", "Summary", "Profile"],
        "prompt": "Write a compelling LinkedIn 'About' section in the first person. Structure: Hook (passion/drive), Career Journey (key milestones), Core Expertise (bulleted list of skills), and Call to Action (networking/collaboration). Background: [BACKGROUND].",
        "exampleInput": "BACKGROUND: UX Designer, loves solving complex workflows, worked in finance and tech, mentor at local design club.",
        "exampleOutput": "I believe that the best design is invisible—it simply works when you need it.\n\nOver the past 6 years, I've designed workflows for financial applications and user portals. My focus is on turning complex database requirements into clean, user-friendly layouts.\n\nMy Expertise:\n• User Research & Testing\n• Wireframing & Prototyping (Figma)\n• Interactive Design Systems\n\nWhen I'm not designing, I mentor junior developers at the local design club. Feel free to connect!",
        "tips": ["Use white space to make it readable.", "Keep the tone professional but personal."]
    },
    {
        "id": "lnk-003",
        "title": "Content Creation Calendar Planner",
        "category": "linkedin",
        "difficulty": "Intermediate",
        "description": "Generates a 4-week thematic content calendar for LinkedIn posts related to your domain.",
        "tags": ["Content Strategy", "Posting", "Personal Brand"],
        "prompt": "Generate a 4-week LinkedIn content calendar (1 post per week) for my profile. Focus on establishing my authority in [DOMAIN]. Each post should have: Topic, Hook suggestion, and Key takeaway.",
        "exampleInput": "DOMAIN: Agile Project Management",
        "exampleOutput": "Week 1: \n• Topic: The misconception of daily standups.\n• Hook: If your daily standup lasts 30 minutes, it's not a standup.\n• Takeaway: Standups are for coordination, not status reports.\n\nWeek 2:\n• Topic: Estimating tasks.\n• Hook: Why story points are better than hours.\n• Takeaway: Estimates are about complexity, not absolute time.",
        "tips": ["Vary the types of posts (e.g. stories, tips, opinion).", "Interact with comments."]
    },
    {
        "id": "lnk-004",
        "title": "LinkedIn Outreach Message (Recruiter)",
        "category": "linkedin",
        "difficulty": "Beginner",
        "description": "Drafts short, high-conversion messages to send to recruiters when applying for a role.",
        "tags": ["Outreach", "Recruiter", "Messaging"],
        "prompt": "Write a LinkedIn message to send to a recruiter. Keep it under 300 characters (LinkedIn connect limit) or under 100 words for an InMail. Include my top achievement and the role I've applied for. Role: [ROLE], Achievement: [ACHIEVEMENT].",
        "exampleInput": "ROLE: Account Executive at Salesforce\nACHIEVEMENT: Exceeded sales quota by 130% last year at Hubspot.",
        "exampleOutput": "Hi [Name],\n\nI recently applied for the Account Executive role and wanted to connect. In my previous role at HubSpot, I exceeded my sales quota by 130%. I'd love to learn more about the team's current goals.\n\nBest,\n[My Name]",
        "tips": ["Keep it personal and direct.", "Double-check the recruiter's name."]
    },
    {
        "id": "lnk-005",
        "title": "Recommendation Request Writer",
        "category": "linkedin",
        "difficulty": "Beginner",
        "description": "Drafts polite requests for LinkedIn recommendations from former managers or peers.",
        "tags": ["Recommendations", "Outreach", "Networking"],
        "prompt": "Write a message requesting a LinkedIn recommendation from a former colleague. Make it easy for them by suggesting a specific project or skill they could focus on. Colleague Name: [NAME], Project: [PROJECT].",
        "exampleInput": "NAME: Marcus (Former Manager)\nPROJECT: Migrating the legacy billing system on-time and under budget.",
        "exampleOutput": "Hi Marcus,\n\nI hope you're doing well. I am updating my LinkedIn profile and would appreciate a recommendation from you regarding our work on the legacy billing system migration. Sharing your perspective on my project management during that launch would be extremely valuable. Thank you!\n\nBest,\n[My Name]",
        "tips": ["Always offer to write them a recommendation in return.", "Customize the request to make it personal."]
    },
    {
        "id": "lnk-006",
        "title": "Featured Post Writer (Achievement Update)",
        "category": "linkedin",
        "difficulty": "Intermediate",
        "description": "Writes a professional announcement post for a new job, certification, or project delivery.",
        "tags": ["Post Writing", "Self Promotion", "Milestone"],
        "prompt": "Draft a LinkedIn post announcing a professional milestone. Tone should be grateful and professional, avoiding sounding boastful. Highlight the team's effort and my key learning. Milestone: [MILESTONE].",
        "exampleInput": "MILESTONE: Launched the new corporate website after 6 months of development.",
        "exampleOutput": "We did it! After 6 months of collaboration, the new corporate website is live. \n\nI want to thank the engineering, design, and product teams for their hard work. This project taught me the importance of clear communication and modular architecture.\n\nCheck it out here: [Link]",
        "tips": ["Tag colleagues who helped.", "Include a high-quality image or link."]
    },
    {
        "id": "lnk-007",
        "title": "LinkedIn Profile Audit Checklist",
        "category": "linkedin",
        "difficulty": "Beginner",
        "description": "Generates an actionable checklist to verify if your profile is set up for 'Open to Work' success.",
        "tags": ["Audit", "Profile", "Visibility"],
        "prompt": "Generate a step-by-step checklist to audit my LinkedIn profile. Ensure the checklist covers search indexing optimization, profile completeness, and settings that attract recruiters. Role target: [ROLE_TARGET].",
        "exampleInput": "ROLE_TARGET: Senior UX Researcher",
        "exampleOutput": "• [ ] Headline: Include 'Senior UX Researcher' and core methodologies (e.g. Usability Testing, Figma).\n• [ ] About: Story-driven summary detailing user research methodologies.\n• [ ] Experience: Use bullet points with metrics for last 3 roles.\n• [ ] Settings: Set 'Open to Work' to recruiters only (unless active search).",
        "tips": ["Turn on 'Creator Mode' to showcase your content.", "Ensure your contact email is visible to connections."]
    },
    {
        "id": "lnk-008",
        "title": "Cold Connection Request (Peer)",
        "category": "linkedin",
        "difficulty": "Beginner",
        "description": "Drafts short connection requests to peers in your field to build an organic network.",
        "tags": ["Networking", "Connection", "Short Form"],
        "prompt": "Write a LinkedIn connection request note to send to a peer working in my industry at a target company. Explain why I want to connect without asking for a job. Details: [DETAILS].",
        "exampleInput": "DETAILS: Connecting with a Senior Software Engineer at Netflix, I want to learn about their engineering culture.",
        "exampleOutput": "Hi [Name],\n\nI saw your profile and admire your work at Netflix. As a fellow Software Engineer, I'd love to connect to keep up with your insights on scalable systems.\n\nBest,\n[My Name]",
        "tips": ["Always customize the invitation note.", "Keep it under 300 characters."]
    },
    {
        "id": "lnk-009",
        "title": "Thought-Leadership Comment Generator",
        "category": "linkedin",
        "difficulty": "Intermediate",
        "description": "Drafts value-adding comments to post on industry leaders' threads to build visibility.",
        "tags": ["Engagement", "Visibility", "Networking"],
        "prompt": "Draft a professional comment for a LinkedIn post about [POST_TOPIC]. The comment should add value, share a brief insight from my experience, and encourage discussion. Topic Details: [TOPIC_DETAILS].",
        "exampleInput": "POST_TOPIC: Remote team building.\nTOPIC_DETAILS: Standard virtual happy hours are dead, we need project-based alignment and virtual workspaces.",
        "exampleOutput": "Great points. Standard happy hours often feel forced. In my experience, building remote connection works best when centered around collaborative workshops or low-stakes hackathons where the team solves a problem together. How has your team structured these sessions?",
        "tips": ["Be respectful and constructive.", "Ask a question to start a conversation."]
    },
    {
        "id": "lnk-010",
        "title": "LinkedIn Engagement Strategy",
        "category": "linkedin",
        "difficulty": "Beginner",
        "description": "Creates a structured daily/weekly engagement routine to build organic reach on LinkedIn.",
        "tags": ["Engagement", "Routine", "Organic Reach"],
        "prompt": "Generate a weekly 15-minute daily routine for LinkedIn engagement. Focus on building relationships and visibility without spending hours writing posts.",
        "exampleInput": "Agile Project Manager",
        "exampleOutput": "Monday: Post 1 thought-provoking update.\nTuesday: Comment on 3 posts in your feed.\nWednesday: Connect with 2 peers.\nThursday: Leave feedback on a post.\nFriday: Share a resource or tool you found useful.",
        "tips": ["Consistency is key.", "Respond to all comments on your posts."]
    }
]
prompts.extend(lnk_data)

# --- 6. NETWORKING PROMPTS (id: net-001 to net-010) ---
net_data = [
    {
        "id": "net-001",
        "title": "Informational Interview Request",
        "category": "networking",
        "difficulty": "Intermediate",
        "description": "Drafts a low-pressure email asking an industry veteran for a 15-minute chat about their career path.",
        "tags": ["Informational Interview", "Outreach", "Mentorship"],
        "prompt": "Write an email requesting a 15-minute informational interview with a professional. Emphasize that I am seeking advice, not a job. Details: [DETAILS].",
        "exampleInput": "DETAILS: Targeted at a Director of Product at Adobe, I am a product management student.",
        "exampleOutput": "Subject: Career Advice Query - Product Management Student\n\nDear [Name],\n\nI hope this email finds you well. I am a Product Management student at [University] and have been following Adobe's product launches.\n\nI would love to request a brief 15-minute virtual chat to learn about your career path. I am seeking advice and would value your perspective.\n\nThank you,\n[My Name]",
        "tips": ["Suggest a specific time and platform.", "Keep the request brief."]
    },
    {
        "id": "net-002",
        "title": "Cold Outreach to Recruiters",
        "category": "networking",
        "difficulty": "Beginner",
        "description": "Drafts clear emails to corporate recruiters introducing your profile for open pipeline roles.",
        "tags": ["Cold Outreach", "Recruiter", "Job Search"],
        "prompt": "Write a cold email to a recruiter introducing myself and explaining my interest in a specific company. Highlight my relevant skills. Details: [DETAILS].",
        "exampleInput": "DETAILS: Software Engineer applying to Google, experienced in cloud systems.",
        "exampleOutput": "Subject: Software Engineer Application Inquiry - [My Name]\n\nDear [Recruiter Name],\n\nI hope you're doing well. I recently applied for the Software Engineer role and wanted to introduce myself. I specialize in cloud systems development.\n\nI've attached my resume and would appreciate the chance to connect.\n\nBest,\n[My Name]",
        "tips": ["Always attach your resume.", "Keep it professional and brief."]
    },
    {
        "id": "net-003",
        "title": "Industry Expert Outreach",
        "category": "networking",
        "difficulty": "Intermediate",
        "description": "Drafts emails asking for feedback on a specific article or project from an industry expert.",
        "tags": ["Feedback", "Expert Outreach", "Professional Development"],
        "prompt": "Draft an email to an industry expert asking for feedback on a project or article I wrote. Context: [CONTEXT].",
        "exampleInput": "CONTEXT: Wrote a paper on data analytics in logistics, asking a logistics professor for feedback.",
        "exampleOutput": "Subject: Feedback Request on Logistics Data Analysis Paper\n\nDear Professor [Name],\n\nI recently wrote a paper analyzing data analytics in logistics and would value your perspective. Having read your research, I believe your feedback would be incredibly helpful.\n\nWould you be open to reviewing a draft?\n\nThank you,\n[My Name]",
        "tips": ["Attach the draft or link to it.", "Be respectful of their time."]
    },
    {
        "id": "net-004",
        "title": "Alumni Connection Outreach",
        "category": "networking",
        "difficulty": "Beginner",
        "description": "Leverages university alumni networks for warm introductions and advice chats.",
        "tags": ["Alumni", "Warm Connection", "Outreach"],
        "prompt": "Write a message to connect with a university alumnus on LinkedIn. Highlight the shared connection of the university. Details: [DETAILS].",
        "exampleInput": "DETAILS: Alumnus from Ohio State University working at Microsoft, I graduated in 2024.",
        "exampleOutput": "Hi [Name],\n\nI saw we both went to OSU (Go Bucks!). I graduated in 2024 and am looking to grow my network in tech. I'd love to connect and learn about your path to Microsoft.\n\nBest,\n[My Name]",
        "tips": ["Mention the shared school early.", "Be friendly and conversational."]
    },
    {
        "id": "net-005",
        "title": "Event Follow-up Message",
        "category": "networking",
        "difficulty": "Beginner",
        "description": "Drafts emails to follow up with contacts met at conferences, meetups, or webinars.",
        "tags": ["Follow-Up", "Conference", "Meetup"],
        "prompt": "Write a follow-up email to someone I met at a networking event. Mention a specific topic we discussed to remind them of our conversation. Details: [DETAILS].",
        "exampleInput": "DETAILS: Met Jane at a local startup meetup, discussed serverless backend databases.",
        "exampleOutput": "Subject: Great connecting at the startup meetup!\n\nHi Jane,\n\nIt was great meeting you at the meetup yesterday. I enjoyed our conversation about serverless databases. Let's stay in touch!\n\nBest,\n[My Name]",
        "tips": ["Send the email within 24 hours.", "Keep it short and friendly."]
    },
    {
        "id": "net-006",
        "title": "Group Discussion Icebreaker",
        "category": "networking",
        "difficulty": "Beginner",
        "description": "Generates prompt topics or questions to spark discussions in professional forums or groups.",
        "tags": ["Icebreaker", "Discussion", "Community"],
        "prompt": "Generate 3 icebreaker questions for a professional group discussion about [TOPIC].",
        "exampleInput": "TOPIC: Future of work / Hybrid models",
        "exampleOutput": "1. What is one hybrid work practice that has saved you the most time?\n2. How do you maintain team culture when working remotely?\n3. What tools do you use to manage project tasks across time zones?",
        "tips": ["Keep questions open-ended.", "Encourage diverse viewpoints."]
    },
    {
        "id": "net-007",
        "title": "Project Collaboration Proposal",
        "category": "networking",
        "difficulty": "Intermediate",
        "description": "Drafts pitches to collaborate with other professionals on open-source, blogs, or side projects.",
        "tags": ["Collaboration", "Proposal", "Project"],
        "prompt": "Write an email proposing a collaboration on a project. Outlines the benefits for both parties. Details: [DETAILS].",
        "exampleInput": "DETAILS: Proposing a collaborative blog series on DevOps security to a cybersecurity writer.",
        "exampleOutput": "Subject: Collaboration Proposal: DevOps Security Blog Series\n\nDear [Name],\n\nI follow your work on cybersecurity and would love to propose a collaboration. I am planning a blog series on DevOps security and believe our combined insights would be valuable.\n\nLet me know if you'd be open to discussing this.\n\nBest,\n[My Name]",
        "tips": ["Focus on the mutual benefits.", "Be clear about the project scope."]
    },
    {
        "id": "net-008",
        "title": "Virtual Coffee Invitation",
        "category": "networking",
        "difficulty": "Beginner",
        "description": "Drafts friendly invitations to check in with existing connections over a quick video call.",
        "tags": ["Virtual Coffee", "Check-in", "Existing Connection"],
        "prompt": "Write a short email inviting a current professional contact to a virtual coffee chat to catch up. Details: [DETAILS].",
        "exampleInput": "DETAILS: Catching up with a former colleague after 6 months.",
        "exampleOutput": "Subject: Catching up / Virtual Coffee?\n\nHi [Name],\n\nIt's been a while! I'd love to catch up and hear what you've been working on. Would you be open to a quick virtual coffee next week?\n\nBest,\n[My Name]",
        "tips": ["Keep the tone casual and friendly.", "Suggest a few time options."]
    },
    {
        "id": "net-009",
        "title": "Introducing Two Contacts",
        "category": "networking",
        "difficulty": "Beginner",
        "description": "Drafts emails to introduce two contacts in your network who would benefit from knowing each other.",
        "tags": ["Introduction", "Connector", "Email"],
        "prompt": "Write an email introducing two contacts in my network. Explain why they should connect. Details: [DETAILS].",
        "exampleInput": "DETAILS: Introducing a freelance graphic designer to a marketer looking for design help.",
        "exampleOutput": "Subject: Introduction: [Designer Name] & [Marketer Name]\n\nHi both,\n\nI wanted to introduce you. [Designer Name] is a fantastic graphic designer, and [Marketer Name] is looking for design support. I hope you find this connection helpful!\n\nBest,\n[My Name]",
        "tips": ["Get consent from both parties first.", "Keep the introduction clear and brief."]
    },
    {
        "id": "net-010",
        "title": "Long-Term Relationship Nurture",
        "category": "networking",
        "difficulty": "Intermediate",
        "description": "Drafts low-key follow-up emails to share resources or updates to keep connections active.",
        "tags": ["Nurturing", "Follow-up", "Relationship"],
        "prompt": "Write an email to nurture a professional relationship. Share a resource or article that reminds me of our conversation. Details: [DETAILS].",
        "exampleInput": "DETAILS: Sharing an article on AI trends with a former mentor.",
        "exampleOutput": "Subject: Interesting article on AI trends / Thought of you!\n\nHi [Name],\n\nI came across this article on AI trends and thought of our conversation last month. I hope you find it interesting!\n\nBest,\n[My Name]",
        "tips": ["Keep the message low-pressure.", "Do not ask for anything in return."]
    }
]
prompts.extend(net_data)

# --- 7. SALARY NEGOTIATION PROMPTS (id: sal-001 to sal-010) ---
sal_data = [
    {
        "id": "sal-001",
        "title": "Initial Counter-Offer Script",
        "category": "salary",
        "difficulty": "Advanced",
        "description": "Drafts a polished email counter-offering a higher base salary after receiving a job offer.",
        "tags": ["Counter-Offer", "Salary Negotiation", "Email Script"],
        "prompt": "Write a professional email counter-offering a higher base salary. Base the argument on my specialized skills and market research. Offer Details: [OFFER_DETAILS] Target Salary: [TARGET_SALARY].",
        "exampleInput": "OFFER_DETAILS: Offered $90,000 for Product Analyst, base market average is $100,000.\nTARGET_SALARY: $105,000.",
        "exampleOutput": "Subject: Job Offer - Product Analyst - [My Name]\n\nDear [Hiring Manager Name],\n\nThank you for the offer. I am excited about the opportunity. Based on my experience and market research, I would like to discuss a base salary of $105,000. \n\nThank you for your consideration.\n\nBest,\n[My Name]",
        "tips": ["Express enthusiasm for the role first.", "Back up your number with research."]
    },
    {
        "id": "sal-002",
        "title": "Total Compensation Checklist Writer",
        "category": "salary",
        "difficulty": "Beginner",
        "description": "Creates a checklist of benefits to negotiate beyond base salary (equity, bonus, PTO, health).",
        "tags": ["Total Comp", "Benefits", "Negotiation"],
        "prompt": "Generate a checklist of total compensation elements I should review and negotiate besides base salary. Details: [DETAILS].",
        "exampleInput": "DETAILS: Senior Dev role at a series B startup.",
        "exampleOutput": "• [ ] Stock Options / Equity (strike price, vesting schedule)\n• [ ] Performance Bonus (percentage, criteria)\n• [ ] Sign-on Bonus\n• [ ] Paid Time Off (PTO) / Vacation days\n• [ ] Remote work flexibility & home office stipend\n• [ ] Professional development allowance",
        "tips": ["Research the market averages.", "Prioritize what matters most to you."]
    },
    {
        "id": "sal-003",
        "title": "Negotiating Signing Bonus",
        "category": "salary",
        "difficulty": "Intermediate",
        "description": "Drafts emails asking for a sign-on bonus to offset lost bonuses or stock options from a former role.",
        "tags": ["Sign-on Bonus", "Offset", "Email"],
        "prompt": "Write an email negotiating a signing bonus to offset compensation I am leaving behind at my current company. Details: [DETAILS].",
        "exampleInput": "DETAILS: Leaving behind a $10,000 annual bonus that pays out next month.",
        "exampleOutput": "Subject: Job Offer Discussion - [My Name]\n\nDear [Name],\n\nThank you for the offer. I am excited to join the team. To offset the $10,000 annual bonus I am leaving behind, would you be open to a one-time sign-on bonus of $10,000?\n\nBest,\n[My Name]",
        "tips": ["Explain the reasoning clearly.", "Be polite and professional."]
    },
    {
        "id": "sal-004",
        "title": "Performance Review Negotiation",
        "category": "salary",
        "difficulty": "Intermediate",
        "description": "Drafts requests to schedule an early performance review cycle if base salary budgets are currently locked.",
        "tags": ["Performance Review", "Evaluation", "Email Request"],
        "prompt": "Write a request to negotiate an early performance review cycle as a compromise if the base salary budget is locked. Details: [DETAILS].",
        "exampleInput": "DETAILS: Budget locked at $85,000, requesting a review in 6 months instead of 12.",
        "exampleOutput": "Subject: Offer Conversation - [My Name]\n\nDear [Name],\n\nThank you for the clarification. Since the budget is currently locked at $85,000, would you be open to scheduling a formal performance and salary review in 6 months?\n\nBest,\n[My Name]",
        "tips": ["Get any agreement in writing.", "Focus on delivering value in the initial months."]
    },
    {
        "id": "sal-005",
        "title": "Handling Lowball Offers",
        "category": "salary",
        "difficulty": "Intermediate",
        "description": "Drafts polite, professional responses to reject or negotiate lowball offers gracefully without burning bridges.",
        "tags": ["Lowball Offer", "Graceful Rejection", "Negotiation"],
        "prompt": "Write a professional response to a job offer that is significantly below my target range. Maintain a positive connection. Details: [DETAILS].",
        "exampleInput": "DETAILS: Offered $60,000 for role, target is $85,000 minimum.",
        "exampleOutput": "Subject: Offer Feedback - [My Name]\n\nDear [Name],\n\nThank you for the offer. I appreciate the opportunity. However, the salary offered is significantly below my target range of $85,000. Let me know if there is room to adjust.\n\nBest,\n[My Name]",
        "tips": ["Be direct but polite.", "Do not sound offended."]
    },
    {
        "id": "sal-006",
        "title": "Equity vs Cash Evaluation Script",
        "category": "salary",
        "difficulty": "Advanced",
        "description": "Generates analytical prompts to evaluate startup equity valuation and compare it against cash offers.",
        "tags": ["Equity", "Startup", "Evaluation"],
        "prompt": "Create a list of questions to evaluate an equity offer from a startup. Details: [DETAILS].",
        "exampleInput": "DETAILS: Offered 0.1% equity in a startup valued at $10M.",
        "exampleOutput": "1. What is the current valuation of the company?\n2. What is the strike price of the options?\n3. What is the vesting schedule (e.g. 4 years, 1-year cliff)?\n4. What is the total number of outstanding shares?\n5. Are there any future dilution expectations?",
        "tips": ["Understand the risks of startup equity.", "Consult a financial advisor if needed."]
    },
    {
        "id": "sal-007",
        "title": "Market Rate Research Outline",
        "category": "salary",
        "difficulty": "Beginner",
        "description": "Creates outlines and resources to search for accurate market compensation data.",
        "tags": ["Market Rate", "Research", "Compensation"],
        "prompt": "Generate a list of resources and search strategies to research market rates for [ROLE] in [LOCATION].",
        "exampleInput": "ROLE: Project Manager\nLOCATION: Chicago, IL",
        "exampleOutput": "• Resources: Glassdoor, Levels.fyi, Indeed, Salary.com\n• Strategies: Search by title variations, filter by location, check industry-specific surveys.",
        "tips": ["Compare data from multiple sources.", "Adjust for cost of living."]
    },
    {
        "id": "sal-008",
        "title": "Salary Negotiation Email Script (B2B)",
        "category": "salary",
        "difficulty": "Advanced",
        "description": "Drafts business-focused emails that align salary increases with projected revenue generation.",
        "tags": ["Business Value", "Email", "Advanced Negotiation"],
        "prompt": "Write a salary negotiation email focused on the revenue and business value I expect to generate. Details: [DETAILS].",
        "exampleInput": "DETAILS: Sales Manager role, aiming for 10% increase, projecting 20% sales growth.",
        "exampleOutput": "Subject: Salary Discussion - [My Name]\n\nDear [Name],\n\nThank you for the offer. Based on my project to drive 20% sales growth, I would like to discuss a base salary increase of 10% to align with this target.\n\nBest,\n[My Name]",
        "tips": ["Align your value with concrete metrics.", "Keep the tone professional."]
    },
    {
        "id": "sal-009",
        "title": "Verbal Negotiation Script",
        "category": "salary",
        "difficulty": "Intermediate",
        "description": "Provides scripts for live phone or video call salary negotiations.",
        "tags": ["Verbal Script", "Phone Call", "Live Negotiation"],
        "prompt": "Write a script for a live phone call negotiation. Include lines for handling common objections. Details: [DETAILS].",
        "exampleInput": "DETAILS: Handling objection: 'We don't have budget for a higher salary'.",
        "exampleOutput": "Objection: We don't have budget.\nResponse: I understand. Would you be open to adjusting benefits or scheduling a review in 6 months?",
        "tips": ["Stay calm and professional.", "Listen carefully to their feedback."]
    },
    {
        "id": "sal-010",
        "title": "Benefits Package Customization",
        "category": "salary",
        "difficulty": "Beginner",
        "description": "Drafts proposals to customize health, wellness, and education perks.",
        "tags": ["Benefits", "Customization", "Proposal"],
        "prompt": "Write a proposal to customize my benefits package to include professional development stipends. Details: [DETAILS].",
        "exampleInput": "DETAILS: Requesting a $2,000 annual allowance for courses.",
        "exampleOutput": "Subject: Benefits Customization - [My Name]\n\nDear [Name],\n\nI would like to request the inclusion of a $2,000 annual professional development allowance in my benefits package.\n\nBest,\n[My Name]",
        "tips": ["Explain how this benefits the company.", "Keep the request reasonable."]
    }
]
prompts.extend(sal_data)

# --- 8. CAREER PLANNING PROMPTS (id: car-001 to car-010) ---
car_data = [
    {
        "id": "car-001",
        "title": "5-Year Career Roadmap Builder",
        "category": "career",
        "difficulty": "Advanced",
        "description": "Generates a structured career development roadmap mapping out milestone goals and required skills.",
        "tags": ["Roadmap", "Milestones", "Career Planning"],
        "prompt": "Create a 5-year career roadmap based on my current role and target destination. Include: 1. Yearly milestones. 2. Skills to acquire each year. 3. Suggested roles. Details: [DETAILS].",
        "exampleInput": "DETAILS: Current: Junior Developer, Target: Software Architect.",
        "exampleOutput": "Year 1: Master senior framework patterns.\nYear 2: Lead system design modules.\nYear 3: Move to Senior Dev role.\nYear 4: Learn cloud architecture.\nYear 5: Shift to Architect role.",
        "tips": ["Review and update your roadmap annually.", "Find a mentor in your target role."]
    },
    {
        "id": "car-002",
        "title": "Skills Gap Assessment",
        "category": "career",
        "difficulty": "Intermediate",
        "description": "Reviews target job requirements and compares them to your resume to highlight skills gaps.",
        "tags": ["Skills Gap", "Assessment", "Analysis"],
        "prompt": "Analyze the skills gap between my current profile and target role. Details: [DETAILS].",
        "exampleInput": "DETAILS: Current: QA Analyst, Target: Automation Architect. Need to learn coding.",
        "exampleOutput": "• Gap: Programming proficiency (Python/JS).\n• Strategy: Complete a software development course and practice writing automated scripts.",
        "tips": ["Prioritize the most critical gaps first.", "Apply new skills to real projects."]
    },
    {
        "id": "car-003",
        "title": "Transition Path Mapping",
        "category": "career",
        "difficulty": "Intermediate",
        "description": "Maps out a step-by-step career path to transition from one discipline to another.",
        "tags": ["Transition", "Mapping", "Career Shift"],
        "prompt": "Create a career path map to transition from [CURRENT] to [TARGET]. Details: [DETAILS].",
        "exampleInput": "DETAILS: Current: Project Manager, Target: Product Manager.",
        "exampleOutput": "Phase 1: Shift focus to product requirements.\nPhase 2: Work closely with developers.\nPhase 3: Apply for Product Manager roles.",
        "tips": ["Leverage your existing project management skills.", "Learn product management methodologies."]
    },
    {
        "id": "car-004",
        "title": "Mentorship Search Strategy",
        "category": "career",
        "difficulty": "Beginner",
        "description": "Generates an action plan to find, approach, and establish professional relationships with mentors.",
        "tags": ["Mentorship", "Outreach", "Strategy"],
        "prompt": "Generate a strategy to find and approach potential mentors in my industry. Details: [DETAILS].",
        "exampleInput": "DETAILS: Seeking a mentor in finance analytics in New York.",
        "exampleOutput": "• Step 1: Identify potential mentors on LinkedIn.\n• Step 2: Send a polite outreach message.\n• Step 3: Schedule a brief coffee chat.",
        "tips": ["Be clear about what you hope to learn.", "Be respectful of their time."]
    },
    {
        "id": "car-005",
        "title": "Professional Brand Builder",
        "category": "career",
        "difficulty": "Intermediate",
        "description": "Defines your unique value proposition, domain expertise, and core messaging strategies.",
        "tags": ["Brand", "Identity", "Personal Branding"],
        "prompt": "Define my professional brand based on my skills and goals. Details: [DETAILS].",
        "exampleInput": "DETAILS: Developer specializing in high-performance web systems and developer tooling.",
        "exampleOutput": "Brand Identity: Performance-focused Web Developer.\nCore Message: Building fast, scalable, and developer-friendly web applications.",
        "tips": ["Keep your messaging consistent across platforms.", "Share your work and insights online."]
    },
    {
        "id": "car-006",
        "title": "Continuing Education Planning",
        "category": "career",
        "difficulty": "Beginner",
        "description": "Recommends certifications, courses, and books to accelerate career growth in your field.",
        "tags": ["Education", "Courses", "Growth"],
        "prompt": "Recommend certifications and courses for [ROLE] to advance to [TARGET].",
        "exampleInput": "ROLE: Scrum Master\nTARGET: Agile Coach",
        "exampleOutput": "• Certifications: ICP-ACC, ICP-ATF, PMI-ACP\n• Courses: Agile Coaching Masterclass\n• Books: 'Coaching Agile Teams' by Lyssa Adkins",
        "tips": ["Choose certifications recognized by employers.", "Apply what you learn to your current work."]
    },
    {
        "id": "car-007",
        "title": "Identifying Leadership Tracks",
        "category": "career",
        "difficulty": "Intermediate",
        "description": "Evaluates options for moving into management versus climbing the individual contributor (IC) technical track.",
        "tags": ["Leadership", "Management", "Career Track"],
        "prompt": "Compare the individual contributor (IC) track vs. the management track for a [ROLE]. Details: [DETAILS].",
        "exampleInput": "DETAILS: Senior Software Engineer evaluating future tracks.",
        "exampleOutput": "• IC Track: Focuses on technical depth, architecture, and mentoring.\n• Management Track: Focuses on team leadership, strategy, and operations.",
        "tips": ["Choose the track that aligns with your strengths and interests.", "Talk to leaders on both tracks."]
    },
    {
        "id": "car-008",
        "title": "Micro-Goals Setting",
        "category": "career",
        "difficulty": "Beginner",
        "description": "Breaks down annual career goals into bite-sized weekly and monthly action items.",
        "tags": ["Goals", "Planning", "Weekly Tasks"],
        "prompt": "Break down my annual goal of [GOAL] into monthly and weekly micro-goals. Details: [DETAILS].",
        "exampleInput": "GOAL: Learn Python and build a portfolio project.",
        "exampleOutput": "• Month 1: Learn syntax basics.\n• Week 1: Complete variables and loops syntax lessons.\n• Month 2: Build simple script.\n• Week 2: Write a script to organize file directories.",
        "tips": ["Keep goals realistic and measurable.", "Celebrate your progress."]
    },
    {
        "id": "car-009",
        "title": "Dealing with Burnout Checklist",
        "category": "career",
        "difficulty": "Beginner",
        "description": "Generates a checklist to self-assess burnout levels and outline workplace boundaries.",
        "tags": ["Burnout", "Wellness", "Workplace Boundaries"],
        "prompt": "Generate a burnout self-assessment checklist and boundary-setting plan. Details: [DETAILS].",
        "exampleInput": "DETAILS: Working 60-hour weeks, feeling constantly tired and unmotivated.",
        "exampleOutput": "• [ ] Assess physical fatigue and sleep quality.\n• [ ] Audit work hours and identify task bottlenecks.\n• [ ] Establish clear boundaries (e.g. no emails after 6 PM).\n• [ ] Schedule regular breaks and self-care activities.",
        "tips": ["Prioritize your health.", "Communicate boundaries with your manager."]
    },
    {
        "id": "car-010",
        "title": "Career Values Alignment",
        "category": "career",
        "difficulty": "Intermediate",
        "description": "Helps you analyze your core work values (compensation, autonomy, impact, balance) to evaluate opportunities.",
        "tags": ["Values", "Alignment", "Evaluation"],
        "prompt": "Help me evaluate a job offer or opportunity based on my core career values: [VALUES]. Details: [DETAILS].",
        "exampleInput": "VALUES: Autonomy, growth, work-life balance\nDETAILS: Offered role at a fast-paced startup with high pay but expected long hours.",
        "exampleOutput": "• Alignment Analysis: The startup offer conflicts with your value of work-life balance, but aligns with growth.\n• Decision Strategy: Negotiate hours or define remote work flexibility.",
        "tips": ["Know your non-negotiables.", "Re-evaluate values as your career evolves."]
    }
]
prompts.extend(car_data)

# --- 9. EMAIL TEMPLATES PROMPTS (id: eml-001 to eml-010) ---
eml_data = [
    {
        "id": "eml-001",
        "title": "Resigning Gracefully",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts a formal resignation email that maintains professional goodwill and details transition plans.",
        "tags": ["Resignation", "Email Template", "Professional"],
        "prompt": "Write a formal resignation email to my manager. Keep it positive and professional. Details: [DETAILS].",
        "exampleInput": "DETAILS: Leaving for a new role, 2 weeks notice, last day is August 15.",
        "exampleOutput": "Subject: Resignation - [My Name]\n\nDear [Manager Name],\n\nPlease accept this email as formal notification of my resignation. My last day will be August 15. I am grateful for the opportunities I've had here.\n\nBest,\n[My Name]",
        "tips": ["Submit your resignation in writing.", "Offer to help with the transition."]
    },
    {
        "id": "eml-002",
        "title": "Recommendation Request",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts formal emails requesting a letter of recommendation for graduate school or roles.",
        "tags": ["Recommendation", "Email Request", "Outreach"],
        "prompt": "Write a formal request for a letter of recommendation. Details: [DETAILS].",
        "exampleInput": "DETAILS: Requesting a letter from a former professor for a graduate program.",
        "exampleOutput": "Subject: Recommendation Request - [My Name]\n\nDear Professor [Name],\n\nI am applying for a graduate program in computer science and would value a letter of recommendation from you. \n\nThank you,\n[My Name]",
        "tips": ["Request recommendations well in advance.", "Provide details about the target program."]
    },
    {
        "id": "eml-003",
        "title": "Project Status Update",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts concise, structured project status emails for stakeholders.",
        "tags": ["Status Update", "Project Management", "Email"],
        "prompt": "Write a project status update email for my stakeholders. Details: [DETAILS].",
        "exampleInput": "DETAILS: Launching the new app dashboard, on-track, pending final QA check.",
        "exampleOutput": "Subject: Project Update: App Dashboard Launch\n\nHi team,\n\nThe app dashboard launch is currently on-track. We are executing final QA checks and expect delivery by Friday.\n\nBest,\n[My Name]",
        "tips": ["Keep updates brief and structured.", "Highlight any roadblocks immediately."]
    },
    {
        "id": "eml-004",
        "title": "Request for Resources",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts clear business requests for software licenses, training budget, or equipment.",
        "tags": ["Request", "Budget", "Resources"],
        "prompt": "Write an email requesting additional resources or budget for my team. Details: [DETAILS].",
        "exampleInput": "DETAILS: Requesting budget for a Figma enterprise license for 3 designers.",
        "exampleOutput": "Subject: Budget Request: Figma Enterprise Licenses\n\nHi [Name],\n\nI'd like to request budget for 3 Figma enterprise licenses to support our design workflow. \n\nBest,\n[My Name]",
        "tips": ["Explain the business value.", "Keep the budget request justified."]
    },
    {
        "id": "eml-005",
        "title": "Meeting Agenda Template",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts clear, structured agendas to send to attendees before a meeting.",
        "tags": ["Meeting Agenda", "Template", "Coordination"],
        "prompt": "Write a meeting agenda email to send to attendees before our session. Details: [DETAILS].",
        "exampleInput": "DETAILS: Design review meeting, 30 minutes, discussing dashboard navigation.",
        "exampleOutput": "Subject: Agenda: Design Review - Dashboard Navigation\n\nHi all,\n\nHere is the agenda for our design review meeting tomorrow:\n• Review user feedback (10 mins)\n• Walkthrough navigation updates (15 mins)\n• Next steps (5 mins)\n\nBest,\n[My Name]",
        "tips": ["Send the agenda at least 24 hours before the meeting.", "Assign roles like note-taker if needed."]
    },
    {
        "id": "eml-006",
        "title": "Application Follow-Up",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts follow-up emails to send after submitting a job application.",
        "tags": ["Follow-Up", "Application", "Email"],
        "prompt": "Write a follow-up email after submitting a job application. Details: [DETAILS].",
        "exampleInput": "DETAILS: Applied for Marketing Coordinator 2 weeks ago, no response yet.",
        "exampleOutput": "Subject: Application Update: Marketing Coordinator - [My Name]\n\nHi [Name],\n\nI wanted to follow up on my application for the Marketing Coordinator position submitted two weeks ago. I remain very interested in the role.\n\nBest,\n[My Name]",
        "tips": ["Wait 1-2 weeks before following up.", "Keep the message brief and polite."]
    },
    {
        "id": "eml-007",
        "title": "Asking for Extension",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts emails to request a deadline extension for a project, assignment, or offer decision.",
        "tags": ["Extension", "Request", "Email"],
        "prompt": "Write a polite email asking for an extension on a deadline. Details: [DETAILS].",
        "exampleInput": "DETAILS: Requesting an extra week on a marketing proposal due to team illness.",
        "exampleOutput": "Subject: Deadline Extension Request: Marketing Proposal\n\nHi [Name],\n\nI would like to request a one-week extension on the marketing proposal due to team capacity constraints. We expect to deliver by next Friday.\n\nBest,\n[My Name]",
        "tips": ["Request extensions as early as possible.", "Explain the reason neutrally."]
    },
    {
        "id": "eml-008",
        "title": "Decline Offer Politely",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts polite, professional emails to reject a job offer while maintaining connections.",
        "tags": ["Decline Offer", "Graceful Rejection", "Email Template"],
        "prompt": "Write an email declining a job offer politely. Details: [DETAILS].",
        "exampleInput": "DETAILS: Declining offer for Senior Analyst, accepted another role closer to home.",
        "exampleOutput": "Subject: Job Offer - Senior Analyst - [My Name]\n\nDear [Name],\n\nThank you for the offer. However, I have accepted another role that aligns closer with my target location. I hope our paths cross again.\n\nBest,\n[My Name]",
        "tips": ["Express gratitude for the opportunity.", "Keep the reason brief and positive."]
    },
    {
        "id": "eml-009",
        "title": "Decline Meeting Invitation",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts polite templates to decline calendar invitations that don't require your presence.",
        "tags": ["Decline Invitation", "Calendar", "Boundary Setting"],
        "prompt": "Write an email declining a meeting invitation politely. Details: [DETAILS].",
        "exampleInput": "DETAILS: Declining a project brainstorming session because of priority workload constraints.",
        "exampleOutput": "Subject: Meeting Decline: Project Brainstorming\n\nHi [Name],\n\nThank you for the invite. Unfortunately, I have a priority conflict during this time. Please send the notes and I will review them.\n\nBest,\n[My Name]",
        "tips": ["Suggest a proxy attendee or ask for recordings if possible.", "Keep boundaries firm but polite."]
    },
    {
        "id": "eml-010",
        "title": "Onboarding Check-In",
        "category": "email",
        "difficulty": "Beginner",
        "description": "Drafts emails for managers to check in on new hires during their first month.",
        "tags": ["Onboarding", "Check-in", "New Hire"],
        "prompt": "Write an onboarding check-in email to a new team member. Details: [DETAILS].",
        "exampleInput": "DETAILS: Checking in on Sarah, a new developer, after her first week.",
        "exampleOutput": "Subject: Week 1 Check-In - Welcome Sarah!\n\nHi Sarah,\n\nI hope your first week went well! Let's schedule a brief check-in next week to discuss your onboarding progression.\n\nBest,\n[My Name]",
        "tips": ["Create a welcoming atmosphere.", "Provide clear guidance for questions."]
    }
]
prompts.extend(eml_data)

# --- 10. BONUS PROMPTS (id: bon-001 to bon-010) ---
bon_data = [
    {
        "id": "bon-001",
        "title": "ChatGPT Custom Instructions Builder",
        "category": "bonus",
        "difficulty": "Advanced",
        "description": "Builds a system prompt configuration to customize ChatGPT's responses for professional tasks.",
        "tags": ["Custom Instructions", "System Prompt", "ChatGPT"],
        "prompt": "Generate custom instructions for ChatGPT. Split them into: 1. What ChatGPT should know about me (background, role, priorities). 2. How ChatGPT should respond (tone, formatting, constraints). Details: [DETAILS].",
        "exampleInput": "DETAILS: Software Engineer, prefers concise answers, code snippets in Python/JS, hates boilerplate explanations.",
        "exampleOutput": "Profile: Software Engineer specializing in backend systems.\nResponse Style: Concise, direct, prioritize code examples. Skip introductions and preachy warnings.",
        "tips": ["Keep custom instructions updated as your goals change.", "Use constraints to enforce quality."]
    },
    {
        "id": "bon-002",
        "title": "Cold Email to VCs (Pitching Startup)",
        "category": "bonus",
        "difficulty": "Advanced",
        "description": "Drafts high-converting cold emails to venture capital firms requesting pitch meetings.",
        "tags": ["Cold Email", "VC Pitching", "Fundraising"],
        "prompt": "Write a cold email pitching my startup to a venture capitalist. Include: Hook, Problem, Solution, Traction/Metrics, and a clear request for a 10-minute call. Details: [DETAILS].",
        "exampleInput": "DETAILS: Startup: Acme Analytics, AI analytics for supply chains, raised $100k seed, looking for $1M, 20% MoM growth.",
        "exampleOutput": "Subject: Supply Chain AI - 20% MoM Growth - Acme Analytics\n\nDear [VC Name],\n\nAcme Analytics builds AI-driven supply chain analytics software. We are currently growing at 20% MoM and looking to raise $1M. Would you be open to a brief call next week?\n\nBest,\n[My Name]",
        "tips": ["Always put traction in the subject line or opening.", "Do research on the VC's portfolio first."]
    },
    {
        "id": "bon-003",
        "title": "Personal Productivity Planner",
        "category": "bonus",
        "difficulty": "Beginner",
        "description": "Generates a structured daily schedule based on time-blocking techniques and energy focus.",
        "tags": ["Productivity", "Time Blocking", "Planning"],
        "prompt": "Generate a daily schedule using time-blocking. Details: [DETAILS].",
        "exampleInput": "DETAILS: Task list: write code (3 hours), meetings (2 hours), email (1 hour), study (1 hour). Peak focus is in the morning.",
        "exampleOutput": "• 09:00 - 12:00: Deep Work (Write code)\n• 12:00 - 13:00: Lunch Break\n• 13:00 - 15:00: Meetings & Admin\n• 15:00 - 16:00: Emails & Communication\n• 16:00 - 17:00: Professional Development (Study)",
        "tips": ["Group similar tasks together.", "Keep buffer times between sessions."]
    },
    {
        "id": "bon-004",
        "title": "Brainstorming Business Ideas",
        "category": "bonus",
        "difficulty": "Intermediate",
        "description": "Generates 5 side-project or startup ideas based on a target market, tech stack, or trend.",
        "tags": ["Brainstorming", "Business Ideas", "Innovation"],
        "prompt": "Generate 5 side-project or startup ideas based on my interests and skills. Details: [DETAILS].",
        "exampleInput": "DETAILS: Skills: Python, data scraping, interest: real estate analytics.",
        "exampleOutput": "1. Local market pricing scraper dashboard.\n2. Automated property alerts matching investment criteria.\n3. Short-term rental yield analyzer tool.\n4. Commercial real estate tenant tracking database.\n5. Real estate agent lead generation assistant.",
        "tips": ["Validate ideas with simple landing pages first.", "Focus on solving real pain points."]
    },
    {
        "id": "bon-005",
        "title": "Presentation Hook Builder",
        "category": "bonus",
        "difficulty": "Beginner",
        "description": "Generates attention-grabbing opening lines for presentations, keynote speeches, or pitches.",
        "tags": ["Presentation", "Hook", "Public Speaking"],
        "prompt": "Generate 3 alternative hooks for a presentation. Topic: [TOPIC].",
        "exampleInput": "TOPIC: Accelerating software release cycles using automated testing.",
        "exampleOutput": "Option 1: Did you know that software bugs cost businesses over $1.7 trillion annually? Let's discuss how automation changes this.\nOption 2: Imagine launching new features daily with zero system downtime. That's the power of automated release testing.\nOption 3: We have all experienced the stress of a failed release. Today, I'll show you how to eliminate that fear.",
        "tips": ["Open with a statistic, a story, or a bold question.", "Keep the hook under 30 seconds."]
    },
    {
        "id": "bon-006",
        "title": "Critical Thinking Frameworks",
        "category": "bonus",
        "difficulty": "Advanced",
        "description": "Applies frameworks like First Principles, Inversion, or Second-Order Effects to analyze a complex problem.",
        "tags": ["Critical Thinking", "Frameworks", "Problem Analysis"],
        "prompt": "Analyze a problem using critical thinking frameworks (e.g. First Principles, Inversion, Second-Order Effects). Problem: [PROBLEM].",
        "exampleInput": "PROBLEM: High developer turnover in a remote team.",
        "exampleOutput": "• Inversion: What actions would encourage MORE developers to leave? (e.g. micromanagement, lack of growth opportunities).\n• Strategy: Address these areas immediately to improve retention.",
        "tips": ["Use inversion to identify hidden blind spots.", "Consider second-order effects before making decisions."]
    },
    {
        "id": "bon-007",
        "title": "Translation / Localization Audit",
        "category": "bonus",
        "difficulty": "Intermediate",
        "description": "Checks localized text for tone, grammatical issues, and cultural appropriateness.",
        "tags": ["Translation", "Localization", "Audit"],
        "prompt": "Audit the following translation for cultural appropriateness, tone accuracy, and grammatical correctness. Source text: [SOURCE] Translated text: [TRANSLATION] Target Locale: [LOCALE].",
        "exampleInput": "SOURCE: Welcome to our SaaS application, we make team collaboration simple!\nTRANSLATION: Bienvenido a nuestra aplicación SaaS, ¡hacemos que la colaboración en equipo sea simple!\nLOCALE: Spain / Professional business environment.",
        "exampleOutput": "The translation is accurate. The tone is professional and friendly, suitable for a business environment in Spain.",
        "tips": ["Translate tone, not just literal words.", "Test localization with native speakers."]
    },
    {
        "id": "bon-008",
        "title": "System Prompt Simulation",
        "category": "bonus",
        "difficulty": "Advanced",
        "description": "Simulates custom roles or characters for testing chatbot response parameters.",
        "tags": ["Simulation", "Testing", "Chatbots"],
        "prompt": "Simulate a specific role/character response based on guidelines. Role Guidelines: [GUIDELINES] Message: [MESSAGE].",
        "exampleInput": "GUIDELINES: Respond as a helpful customer support agent who is extremely polite and uses emojis.\nMESSAGE: My package is late, where is it?",
        "exampleOutput": "Hello! 📦 I'm so sorry to hear your package is delayed. Let me check the tracking details for you right away! 🔍",
        "tips": ["Define constraints and edge cases in the guidelines.", "Verify responses for safety and alignment."]
    },
    {
        "id": "bon-009",
        "title": "Code Review Prompt Chain",
        "category": "bonus",
        "difficulty": "Advanced",
        "description": "Runs a step-by-step code review for efficiency, readability, and security issues.",
        "tags": ["Code Review", "Quality", "Refactoring"],
        "prompt": "Review this code for quality, performance, and security issues. Suggest clean refactoring. Code: [CODE] Language: [LANGUAGE].",
        "exampleInput": "CODE: \ndef get_users(db):\n    cursor = db.cursor()\n    cursor.execute(\"SELECT * FROM users WHERE id = \" + str(user_id)) # Vulnerable!\n    return cursor.fetchall()\nLANGUAGE: Python",
        "exampleOutput": "Security Vulnerability: SQL Injection vulnerability on line 3. \nRefactoring: Use parameterized queries to prevent SQL injections: \n`cursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))`",
        "tips": ["Prioritize security issues first.", "Include comments in refactoring code suggestions."]
    },
    {
        "id": "bon-010",
        "title": "Research Paper Summarizer",
        "category": "bonus",
        "difficulty": "Intermediate",
        "description": "Summarizes long research papers or technical documents into structured notes.",
        "tags": ["Summarization", "Research", "Technical Notes"],
        "prompt": "Summarize the key findings, methodologies, and conclusions of the attached text or paper summary. Text: [TEXT].",
        "exampleInput": "TEXT: Long text explaining the research and findings of a new AI model that generates code.",
        "exampleOutput": "• Key Finding: The new AI model improves code generation accuracy by 15%.\n• Methodology: Trained on 1TB of open-source repositories and tested using unit tests.\n• Conclusion: Automated coding assistants are becoming highly reliable.",
        "tips": ["Highlight any limitations identified by the authors.", "Use bullet points for readability."]
    }
]
prompts.extend(bon_data)

# Ensure data folder exists
os.makedirs("../data", exist_ok=True)

# Write to prompts.json
with open("../data/prompts.json", "w", encoding="utf-8") as f:
    json.dump(prompts, f, indent=2, ensure_ascii=False)

# Write to prompts.js
with open("../data/prompts.js", "w", encoding="utf-8") as f:
    f.write("// Automatically generated database for offline PromptVault\n")
    f.write("window.PROMPTS_DATA = ")
    json.dump(prompts, f, indent=2, ensure_ascii=False)
    f.write(";\n")

print(f"Generated {len(prompts)} prompts in data/prompts.json and data/prompts.js!")
