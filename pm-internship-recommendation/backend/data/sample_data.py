def get_sample_internships():
    """
    Sample internship data for testing
    In production, this would come from a database
    """
    return [
        {
            "id": 1,
            "title": "Software Development Intern",
            "company": "TechCorp India",
            "location": "Bangalore",
            "duration": "3 months",
            "stipend": "₹15,000/month",
            "sector": "Technology",
            "description": "Work on web development projects using React and Node.js. Learn modern software development practices and contribute to real-world applications.",
            "requirements": {
                "education": "B.Tech/B.Sc in Computer Science or related field",
                "skills": ["JavaScript", "React", "Node.js", "HTML", "CSS"],
                "experience": "Fresher"
            },
            "application_deadline": "2024-02-15",
            "posted_date": "2024-01-15"
        },
        {
            "id": 2,
            "title": "Digital Marketing Intern",
            "company": "MarketPro Solutions",
            "location": "Mumbai",
            "duration": "6 months",
            "stipend": "₹12,000/month",
            "sector": "Marketing",
            "description": "Assist in creating digital marketing campaigns, social media management, and content creation. Learn SEO, SEM, and analytics tools.",
            "requirements": {
                "education": "Any graduate degree",
                "skills": ["Social Media", "Content Writing", "SEO", "Marketing"],
                "experience": "Fresher to 1 year"
            },
            "application_deadline": "2024-02-20",
            "posted_date": "2024-01-18"
        },
        {
            "id": 3,
            "title": "Data Analytics Intern",
            "company": "DataInsights Ltd",
            "location": "Pune",
            "duration": "4 months",
            "stipend": "₹18,000/month",
            "sector": "Technology",
            "description": "Analyze business data using Python and SQL. Create visualizations and reports to support business decisions.",
            "requirements": {
                "education": "B.Tech/M.Tech/B.Sc in relevant field",
                "skills": ["Python", "SQL", "Data Analysis", "Excel", "Tableau"],
                "experience": "Fresher"
            },
            "application_deadline": "2024-02-10",
            "posted_date": "2024-01-12"
        },
        {
            "id": 4,
            "title": "Finance Intern",
            "company": "SecureBank",
            "location": "Delhi",
            "duration": "6 months",
            "stipend": "₹20,000/month",
            "sector": "Finance",
            "description": "Support financial analysis, budgeting, and reporting activities. Learn about banking operations and financial modeling.",
            "requirements": {
                "education": "B.Com/MBA/M.Com in Finance",
                "skills": ["Excel", "Financial Analysis", "Accounting", "Communication"],
                "experience": "Fresher to 2 years"
            },
            "application_deadline": "2024-02-25",
            "posted_date": "2024-01-20"
        },
        {
            "id": 5,
            "title": "Mechanical Engineering Intern",
            "company": "AutoTech Manufacturing",
            "location": "Chennai",
            "duration": "6 months",
            "stipend": "₹16,000/month",
            "sector": "Engineering",
            "description": "Work on mechanical design projects using CAD software. Assist in product development and testing processes.",
            "requirements": {
                "education": "B.Tech in Mechanical Engineering",
                "skills": ["AutoCAD", "SolidWorks", "Problem Solving", "Teamwork"],
                "experience": "Fresher"
            },
            "application_deadline": "2024-02-18",
            "posted_date": "2024-01-16"
        },
        {
            "id": 6,
            "title": "Content Writing Intern",
            "company": "Creative Media House",
            "location": "Hyderabad",
            "duration": "4 months",
            "stipend": "₹10,000/month",
            "sector": "Media",
            "description": "Create engaging content for websites, blogs, and social media. Learn content strategy and digital storytelling.",
            "requirements": {
                "education": "BA/MA in English, Journalism, or related field",
                "skills": ["Content Writing", "Communication", "Social Media", "Research"],
                "experience": "Fresher"
            },
            "application_deadline": "2024-02-12",
            "posted_date": "2024-01-14"
        },
        {
            "id": 7,
            "title": "Business Development Intern",
            "company": "GrowthVentures",
            "location": "Gurgaon",
            "duration": "5 months",
            "stipend": "₹14,000/month",
            "sector": "Business",
            "description": "Support business development activities, market research, and client relationship management.",
            "requirements": {
                "education": "MBA/B.Com/BBA",
                "skills": ["Communication", "Business Analysis", "Research", "Excel"],
                "experience": "Fresher to 1 year"
            },
            "application_deadline": "2024-02-22",
            "posted_date": "2024-01-19"
        },
        {
            "id": 8,
            "title": "Graphic Design Intern",
            "company": "DesignStudio Pro",
            "location": "Ahmedabad",
            "duration": "3 months",
            "stipend": "₹8,000/month",
            "sector": "Design",
            "description": "Create visual designs for digital and print media. Work on branding projects and learn design principles.",
            "requirements": {
                "education": "Diploma/Degree in Design or related field",
                "skills": ["Photoshop", "Illustrator", "Figma", "Creative Thinking"],
                "experience": "Fresher"
            },
            "application_deadline": "2024-02-08",
            "posted_date": "2024-01-10"
        },
        {
            "id": 9,
            "title": "Research Intern",
            "company": "Innovation Labs",
            "location": "Kolkata",
            "duration": "4 months",
            "stipend": "₹12,000/month",
            "sector": "Research",
            "description": "Conduct research on emerging technologies and market trends. Prepare research reports and presentations.",
            "requirements": {
                "education": "M.Tech/M.Sc/PhD in relevant field",
                "skills": ["Research", "Analysis", "Writing", "Presentation"],
                "experience": "Fresher to 2 years"
            },
            "application_deadline": "2024-02-28",
            "posted_date": "2024-01-22"
        },
        {
            "id": 10,
            "title": "HR Intern",
            "company": "PeopleFirst Consulting",
            "location": "Jaipur",
            "duration": "3 months",
            "stipend": "₹11,000/month",
            "sector": "Human Resources",
            "description": "Assist in recruitment processes, employee engagement activities, and HR documentation.",
            "requirements": {
                "education": "MBA in HR/Psychology/Related field",
                "skills": ["Communication", "Leadership", "Excel", "Problem Solving"],
                "experience": "Fresher"
            },
            "application_deadline": "2024-02-14",
            "posted_date": "2024-01-13"
        },
        {
            "id": 11,
            "title": "Mobile App Development Intern",
            "company": "AppTech Solutions",
            "location": "Remote",
            "duration": "4 months",
            "stipend": "₹17,000/month",
            "sector": "Technology",
            "description": "Develop mobile applications for Android and iOS platforms. Learn cross-platform development tools.",
            "requirements": {
                "education": "B.Tech in Computer Science or related",
                "skills": ["React Native", "Flutter", "JavaScript", "Mobile Development"],
                "experience": "Fresher"
            },
            "application_deadline": "2024-02-16",
            "posted_date": "2024-01-15"
        },
        {
            "id": 12,
            "title": "Sales Intern",
            "company": "SalesForce India",
            "location": "Lucknow",
            "duration": "6 months",
            "stipend": "₹13,000/month + Incentives",
            "sector": "Sales",
            "description": "Support sales team in lead generation, customer outreach, and sales presentations. Learn CRM tools.",
            "requirements": {
                "education": "Any graduate degree",
                "skills": ["Communication", "Persuasion", "Excel", "Customer Service"],
                "experience": "Fresher"
            },
            "application_deadline": "2024-02-26",
            "posted_date": "2024-01-21"
        },
        # Multilingual sample internships to demonstrate Indic NLP capabilities
        {
            "id": 13,
            "title": "प्रौद्योगिकी प्रशिक्षु", # Technology Trainee in Hindi
            "company": "तकनीकी समाधान प्राइवेट लिमिटेड",
            "location": "नई दिल्ली",
            "duration": "6 महीने",
            "stipend": "₹16,000/माह",
            "sector": "प्रौद्योगिकी",
            "description": "सॉफ्टवेयर विकास में काम करें। वेब एप्लिकेशन बनाना और आधुनिक प्रौद्योगिकी सीखें।",
            "requirements": {
                "education": "कंप्यूटर विज्ञान में बी.टेक",
                "skills": ["पायथन", "जावास्क्रिप्ट", "रिएक्ट", "सॉफ्टवेयर विकास"],
                "experience": "नवा व्यक्ति"
            },
            "application_deadline": "2024-03-01",
            "posted_date": "2024-01-25"
        },
        {
            "id": 14,
            "title": "డిజిటల్ మార్కెటింగ్ ఇంటర్న్", # Digital Marketing Intern in Telugu
            "company": "క్రీఏటివ్ మీడియా హైదరాబాద్",
            "location": "హైదరాబాద్",
            "duration": "4 నెలలు",
            "stipend": "₹14,000/నెల",
            "sector": "మార్కెటింగ్",
            "description": "డిజిటల్ మార్కెటింగ్ క్యాంపెయిన్ల్ మరియు కంటెంట్ అడినిస్ట్రేషన్లో పనిచేయండి। సోషల్ మీడియా మధ్ధ SEO నర్చండి।",
            "requirements": {
                "education": "ఎవరి గ్రాడుఏషన్ రేటు",
                "skills": ["సోషల్ మీడియా", "కంటెంట్ రాస్తు", "SEO", "డిజిటల్ మార్కెటింగ్"],
                "experience": "కొత్తవారు"
            },
            "application_deadline": "2024-03-05",
            "posted_date": "2024-01-28"
        },
        {
            "id": 15,
            "title": "ஆராய்ச்சி பயிற்சி", # Research Trainee in Tamil
            "company": "அறிவியல் ஆராய்ச்சி கேந்திரம்",
            "location": "சென்னை",
            "duration": "5 மாதங்கள்",
            "stipend": "₹15,000/மாதம்",
            "sector": "ஆராய்ச்சி",
            "description": "கணினி அறிவியல் மற்றும் நுணையறிவியல் தொழில்நுட்பங்களில் ஆராய்ச்சி செய்யவும்। அறிக்கை பதிப்பகங்கள் மற்றும் அறிக்கை விளக்கங்கள் தயாரிக்கவும்।",
            "requirements": {
                "education": "இயன்திரவியல் அல்லது மேற்களவி கல்வியில் இருந்த படிப்பு",
                "skills": ["ஆராய்ச்சி", "தரவு பிரிப்பு", "அறிக்கை விளக்கம்", "கணினி"],
                "experience": "புதியவர்"
            },
            "application_deadline": "2024-03-10",
            "posted_date": "2024-02-01"
        },
        {
            "id": 16,
            "title": "সফটওয়্যার ডেভেলপমেন্ট ইন্টার্ন", # Software Development Intern in Bengali
            "company": "টেক সলিউশন্স বাংলাদেশ",
            "location": "কলকাতা",
            "duration": "6 মাস",
            "stipend": "₹17,000/মাস",
            "sector": "প্রযুক্তি",
            "description": "ওয়েব এপ্লিকেশন ডেভেলপমেন্টে কাজ করুন। আধুনিক প্রযুক্তি ও প্রোগ্রামিং ভাষা শেখার সুযোগ।",
            "requirements": {
                "education": "কম্পিউটার সাইন্সে স্নাতক বা সমতুল্য",
                "skills": ["জাভাস্ক্রিপ্ট", "পাইথন", "রিয়্যাক্ট", "প্রোগ্রামিং"],
                "experience": "নতুন"
            },
            "application_deadline": "2024-03-15",
            "posted_date": "2024-02-05"
        }
    ]
