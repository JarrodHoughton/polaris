# Adding Integrated Persistence Layer to Polaris
- Polaris has cleverly created an interface for persistence which can be implemented
- Currently as of 05/09/2024, the only prebuilt implementation options are In-Memory as a binary tree or EclipseLink which is an ORM framework for Java

# Polaris EclipseLink Support
- EclipseLink as a persistent store layer allows us to connect Polaris with a few different databases, the current steps that follow show the setup for a Postgres db 
- [EclipseLink Supported Databases](https://eclipse.dev/eclipselink/documentation/2.4/concepts/app_tl_ext001.htm)
- Currently added postgres as the persistence store for this repo
- Required updated to ./gradle/libs.versions.toml
    - Added dependency **postgresql = { module = "org.postgresql:postgresql", version = "42.6.0" }** under libraries
    - ```
        [libraries]
        postgresql = { module = "org.postgresql:postgresql", version = "42.6.0" }
        rest of library dependencies...
        ```
- Required update to ./extension/persistence/eclipselink/src/main/resource/META-INF/persistence.xml
    - This is to configure EclipseLink to connect to specified database and jdbc connection
    - Here we provide the jdbc connection details: url, username, password
    - For Postgres:
    -   ```
            <properties>
                <property name="jakarta.persistence.jdbc.driver" value="org.postgresql.Driver" />
                <property name="jakarta.persistence.jdbc.url" value="jdbc:postgresql://postgres:5432/{realm}" />
                <property name="jakarta.persistence.jdbc.user" value="postgres" />
                <property name="jakarta.persistence.jdbc.password" value="password" />
            </properties>
        ```
    - Note that Postgres database requires default-realm as a database for Polaris to initialize its tables and populate with principal user + credentials
    - Also note that '{realm}' is required at the end of the DB url as this is replaced dynamically with the database name at runtime
    - Took me a while to figure that out lol
    - **TODO:** configure persistence.xml file to pull in environment variables or could configure to pull from AWS Secrets Manager, depending on environment maybe?
- Required update to ./extension/persistence/eclipselink/build.gradle.kts
    - include dependency for postgres
    - ```
        dependencies {
            implementation(libs.postgresql)
            rest of dependencies...
        }
        ```

# Finally, Run the Polaris Stack:
```
    docker compose -f docker-compose-jupyter.yml up --build
```
- or without build
```
    docker compose -f docker-compose-jupyter.yml up
```