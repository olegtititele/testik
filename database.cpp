// #pragma once

#include <string>
#include <iostream>
#include <pqxx/pqxx>

int main()
{
    std::string connectionString = "host=localhost port=5432 dbname=bot_users user=username password =password";

    try
    {
        pqxx::connection connectionObject(connectionString.c_str());

        pqxx::work worker(connectionObject);

        pqxx::result response = worker.exec("CREATE TABLE users (`user_id` VARCHAR(255), `username` VARCHAR(255)");

        // for (size_t i = 0; i < response.size(); i++)
        // {
        //     std::cout << "Id: " << response[i][0] << " Username: " << response[i][1] << " Password: " << response[i][2] << " Email: " << response[i][3] << std::endl;
        // }
    }
    catch (const std::exception& e)
    {
        std::cerr << e.what() << std::endl;
    }

    system("pause");
}