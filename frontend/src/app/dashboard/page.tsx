"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function AllLinksPage() {
  const [username, setUsername] = useState("");
  const router = useRouter();

  useEffect(() => {
    const loggedInUser = localStorage.getItem("loggedInUser");
    if (loggedInUser) {
      setUsername(loggedInUser);
    } else {
      router.push("/login");
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("loggedInUser");
    router.push("/login");
  };

  if (!username) {
    return null; // Or a loading spinner while redirecting
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-2xl p-8 space-y-8 bg-white rounded-lg shadow-md">
        <div className="flex justify-between items-center">
          <h2 className="text-3xl font-extrabold text-gray-900">
            Welcome, {username}!
          </h2>
          <button onClick={handleLogout} className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
            Logout
          </button>
        </div>
        
        <p className="text-center text-sm text-gray-600">
            Please select an option below:
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
          <Link href="/deposit" className="p-6 text-left border rounded-xl hover:text-blue-600 focus:text-blue-600">
            <h3 className="text-2xl font-bold">Deposit Funds &rarr;</h3>
            <p className="mt-4 text-xl">
              Add money to your account.
            </p>
          </Link>

          <Link href="/transfer" className="p-6 text-left border rounded-xl hover:text-blue-600 focus:text-blue-600">
            <h3 className="text-2xl font-bold">Bank Transfer &rarr;</h3>
            <p className="mt-4 text-xl">
              Send money to another account.
            </p>
          </Link>

          <Link href="/balance" className="p-6 text-left border rounded-xl hover:text-blue-600 focus:text-blue-600">
            <h3 className="text-2xl font-bold">View Balance &rarr;</h3>
            <p className="mt-4 text-xl">
              Check your current account balance.
            </p>
          </Link>

           <Link href="/withdraw" className="p-6 text-left border rounded-xl hover:text-blue-600 focus:text-blue-600">
             <h3 className="text-2xl font-bold">Withdraw Funds &rarr;</h3>
             <p className="mt-4 text-xl">
              Withdraw money from your account.
             </p>
           </Link>
        </div>
      </div>
    </div>
  );
}
