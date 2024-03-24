"use client";
import { useUserStore } from "@/util/userStore";

export default function Home() {
  const { user, login } = useUserStore();

  const handleAdminLogin = () => {
    login("admin@test.com", "admin1234");
  };

  const handleMemberLogin = () => {
    login("member@test.com", "member1234");

  };


  return (
    <main>
      <div className="flex justify-center items-center bg-green-300 m-4 p-4 gap-4">
        {!user && (
          <div className="text-center flex flex-col justify-start gap-8">
            <h1 className="text-3xl font-bold">Welcome to Lost and Found Application</h1>
            <h2>
              For the purpose of testing, please use one of the pre-set login
              buttons
            </h2>
            <div className="flex justify-center gap-8">
              <button
                className="bg-blue-400 hover:bg-green-500 p-2 rounded-xl duration-500"
                onClick={handleAdminLogin}
              >
                Login as Admin User
              </button>
              <button
                className="bg-blue-400 hover:bg-green-500 p-2 rounded-xl duration-500"
                onClick={handleMemberLogin}
              >
                Login as Member User
              </button>
            </div>
          </div>
        )}

        {user && (
          <div className="flex flex-col items-center justify-center">
            <h1 className="text-3xl font-bold mb-8">Welcome</h1>
            <p className="bg-blue-300 text-black font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-300">
              You are now logged in as <span className="text-yellow-800 uppercase">{user.role}</span>
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
