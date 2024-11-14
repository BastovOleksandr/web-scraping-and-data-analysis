# Full list of possible categories you can find on https://jobs.dou.ua/
# The category name must exactly match the one indicated on the website
CATEGORY = "Python"

# List of technologies you want to look for
# ':' symbol can be used to find more diverse recording formats
# example 'js:javascript:java script' will look
# for 'js', 'javascript', 'java script'
# Don't insert spaces around ':' symbol
# Don't insert ':' at the beginning and the end of the string
# the most 'left' option will be written in a file if found
# case-insensitive
TECHNOLOGIES = [
    "python",
    "git",
    "sql",
    "rest",
    "docker",
    "aws",
    "linux",
    "django",
    "postgresql",
    "js:javascript",
    "machine learning:ml",
    "react",
    "oop",
    "flask",
    "nosql",
    "networking",
    "fullstack:full stack",
    "microservice",
    "mongodb",
    "html",
    "css",
    "algorithms",
    "drf:django rest framework",
    "fastapi:fast api",
    "asyncio",
    "graphql",
    "celery",
    "redis",
    "telegram bot",
    "tdd",
    "solid",
    "trello",
    "agile",
    "scrapy",
    "pandas",
    "numpy",
    "matplotlib",
    "tableau",
    "scala",
    "ci/cd",
    "kubernetes"
]

# Try increasing it if your internet connection
# is unstable or has very low speed
# You also can try decrease it too, if you want to scrape data faster. This
# may result in data being collected incompletely
SLEEP_TIMER = 0.3
