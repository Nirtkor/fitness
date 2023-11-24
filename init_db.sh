docker run -d --name cow_project -p 38790:5432 \
-v $HOME/postgresql/hotels_pr:/var/lib/postgresql/cow_project \
-e POSTGRES_PASSWORD=admin \
-e POSTGRES_USER=admin \
-e POSTGRES_DB=fitness_club \
postgres

psql -h 127.0.0.1 -p 38790 -U app fitness_club -f init_db.ddl