db.createUser(
        {
            user: "restapp",
            pwd: "restappadmin",
            roles: [
                {
                    role: "readWrite",
                    db: "docdb"
                }
            ]
        }
);