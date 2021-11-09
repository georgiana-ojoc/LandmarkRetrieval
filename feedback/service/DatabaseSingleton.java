/* 
Singleton will be used by Beans (Spring).
<bean id="example" class="com.Database" scope="singleton">
        --
</bean>
*/


//general SingletonDP example
public class DatabaseSingleton {
    private static Database dataBase = new Database();

    private Database() {
    }

    public static DatabaseSingleton getConnection() {
        return dataBase;
    }

}

