import random

from faker import Faker
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction

from app_hello.models import (
    Profile,
    Experience,
    Education,
    Project,
    Skill,
)


class Command(BaseCommand):
    help = "Create 50 fake users with complete resume data"

    def handle(self, *args, **options):
        choice = input("Delete all NON-superuser users before seeding? (Y/n) ")
        if choice == "Y":
            # superusers are kept so you don't lose your admin login
            User.objects.filter(is_superuser=False).delete()

        fake = Faker("en_US")

        USER_COUNT = 50
        PASSWORD = "Test@12345"

        first_names = [
            "James", "John", "Robert", "Michael", "William",
            "David", "Daniel", "Matthew", "Andrew", "Joseph",
            "Thomas", "Christopher", "Anthony", "Benjamin", "Samuel",
            "Alexander", "Henry", "Jack", "Lucas", "Ethan",
        ]

        last_names = [
            "Anderson", "Brown", "Clark", "Davis", "Evans",
            "Garcia", "Harris", "Johnson", "Lewis", "Martin",
            "Miller", "Moore", "Parker", "Roberts", "Smith",
            "Taylor", "Thomas", "Walker", "White", "Wilson",
        ]

        job_titles = [
            "Software Engineer", "Backend Developer", "Frontend Developer",
            "Full Stack Developer", "Python Developer", "Django Developer",
            "Data Analyst", "Data Scientist", "DevOps Engineer",
            "Mobile App Developer", "UI/UX Designer", "Product Designer",
            "Cybersecurity Analyst", "Machine Learning Engineer",
            "Database Administrator",
        ]

        skills = [
            "Python", "Django", "JavaScript", "React", "HTML", "CSS", "SQL",
            "MySQL", "PostgreSQL", "Git", "Docker", "REST API", "FastAPI",
            "Java", "C++", "C#", "Linux", "AWS", "Machine Learning",
            "Data Analysis",
        ]

        universities = [
            "University of California", "University of Toronto",
            "University of Melbourne", "University of Manchester",
            "University of Amsterdam", "Technical University of Munich",
            "University of Sydney", "University of British Columbia",
            "University of Washington", "University of Texas",
        ]

        degrees = ["Diploma", "associate", "bachelor", "master", "phd"]

        interests = [
            "Programming", "Technology", "Reading", "Travel", "Photography",
            "Open Source", "Artificial Intelligence", "Cybersecurity",
            "Design", "Fitness",
        ]

        project_names = [
            "E-Commerce Platform", "Task Management System",
            "Online Learning Platform", "Employee Management System",
            "Personal Finance Tracker", "Social Media Application",
            "Real Estate Platform", "Healthcare Management System",
            "Inventory Management System", "Job Recruitment Platform",
        ]

        def place():
            # model max_length for location is 50
            return f"{fake.city()}, {fake.country()}"[:50]

        self.stdout.write("Creating fake resume data...")

        password_hash = make_password(PASSWORD)

        # ---------------------------------------------------------
        # Build unique usernames / User objects (not saved yet)
        # ---------------------------------------------------------
        usernames = set(User.objects.values_list("username", flat=True))
        new_users = []
        new_usernames = []

        for _ in range(USER_COUNT):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)

            while True:
                username = (
                    f"{first_name.lower()}.{last_name.lower()}."
                    f"{random.randint(1000, 999999)}"
                )
                if username not in usernames:
                    usernames.add(username)
                    break

            new_usernames.append(username)
            new_users.append(
                User(
                    username=username,
                    email=f"{username}@example.com",
                    password=password_hash,
                    first_name=first_name,
                    last_name=last_name,
                )
            )

        with transaction.atomic():

            # -----------------------------------------------------
            # Users
            # -----------------------------------------------------
            User.objects.bulk_create(new_users, batch_size=100)
            # re-fetch so every user surely has its primary key
            users = list(User.objects.filter(username__in=new_usernames))

            # -----------------------------------------------------
            # Profiles
            # -----------------------------------------------------
            profiles = []
            for user in users:
                job_title = random.choice(job_titles)
                profiles.append(
                    Profile(
                        user=user,
                        phone=fake.phone_number()[:50],
                        job_title=job_title,
                        location=place()[:70],
                        description=(
                            f"{user.first_name} is a motivated "
                            f"{job_title.lower()} with several years "
                            f"of experience building reliable and "
                            f"scalable software solutions. "
                            f"They enjoy solving complex technical "
                            f"problems and working with modern "
                            f"technologies."
                        ),
                        intrests=", ".join(random.sample(interests, 4)),
                    )
                )

            Profile.objects.bulk_create(profiles, batch_size=100)
            # re-fetch profiles (with pk) of the new users
            profiles = list(Profile.objects.filter(user__in=users))

            # -----------------------------------------------------
            # Experiences
            # -----------------------------------------------------
            experiences = []
            for profile in profiles:
                for position in random.sample(job_titles, random.randint(2, 4)):
                    start_year = random.randint(2016, 2022)
                    end_year = random.randint(start_year + 1, 2026)

                    experiences.append(
                        Experience(
                            profile=profile,
                            title=fake.company()[:100],
                            location=place(),
                            date_range=f"{start_year} - {end_year}",
                            position=position,
                            # model max_length is 100
                            job_description=(
                                "Built and maintained software, improved "
                                "performance and shipped new features."
                            ),
                        )
                    )

            Experience.objects.bulk_create(experiences, batch_size=500)

            # -----------------------------------------------------
            # Education
            # -----------------------------------------------------
            educations = []
            for profile in profiles:
                for university in random.sample(universities, random.randint(1, 2)):
                    start_year = random.randint(2012, 2020)
                    end_year = random.randint(
                        start_year + 3,
                        min(start_year + 6, 2026),
                    )

                    educations.append(
                        Education(
                            profile=profile,
                            university=university,
                            location=place(),
                            date_range=f"{start_year} - {end_year}",
                            degree=random.choice(degrees),
                            # model max_length is 100
                            study_description=(
                                "Studied software development, algorithms, "
                                "databases and modern computing."
                            ),
                        )
                    )

            Education.objects.bulk_create(educations, batch_size=200)

            # -----------------------------------------------------
            # Projects
            # -----------------------------------------------------
            projects = []
            for profile in profiles:
                for title in random.sample(project_names, random.randint(2, 4)):
                    projects.append(
                        Project(
                            profile=profile,
                            title=title,
                            description=(
                                "Designed and developed a modern "
                                "application with authentication, "
                                "database integration, responsive "
                                "interfaces, and RESTful API "
                                "functionality."
                            ),
                        )
                    )

            Project.objects.bulk_create(projects, batch_size=500)

            # -----------------------------------------------------
            # Skills
            # -----------------------------------------------------
            skill_objects = []
            for profile in profiles:
                for skill in random.sample(skills, random.randint(6, 10)):
                    skill_objects.append(
                        Skill(
                            profile=profile,
                            title=skill,
                            level=random.randint(1, 5),
                        )
                    )

            Skill.objects.bulk_create(skill_objects, batch_size=500)

        # ---------------------------------------------------------
        # Done
        # ---------------------------------------------------------
        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(users)} fake users!"))
        self.stdout.write(self.style.SUCCESS(f"Created {len(profiles)} profiles."))
        self.stdout.write(self.style.SUCCESS(f"Created {len(experiences)} experiences."))
        self.stdout.write(self.style.SUCCESS(f"Created {len(educations)} education records."))
        self.stdout.write(self.style.SUCCESS(f"Created {len(projects)} projects."))
        self.stdout.write(self.style.SUCCESS(f"Created {len(skill_objects)} skills."))
        self.stdout.write(self.style.SUCCESS(f"Password for all users: {PASSWORD}"))
