#image-search
FROM base

EXPOSE 8083

ENV SQLITE_DATABASE=sqlite:////isat/data/data.db

CMD ["poetry", "run", "python", "-m", "uvicorn", "isat.imageSearch.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
