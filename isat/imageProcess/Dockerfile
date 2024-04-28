#image-processing
FROM base

EXPOSE 8081

ENV SQLITE_DATABASE=sqlite:////isat/data/data.db

CMD ["poetry", "run", "python", "-m", "uvicorn", "isat.imageProcess.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
