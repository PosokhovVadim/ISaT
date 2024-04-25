#color-search
FROM base

EXPOSE 8082

ENV SQLITE_DATABASE=sqlite:////isat/data/data.db

CMD ["poetry", "run", "python", "-m", "uvicorn", "isat.colorSearch.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
