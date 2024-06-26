'use client'
import React, { useState, useEffect } from "react";
import { useSession } from "next-auth/react";
import { VitalLoader } from "../components/icons/VitalLoader";

function DashboardPage() {
  const session = useSession();

  const [isSignedIn, setIsSignedIn] = useState(false);
  const [promptsAndResponses, setPromptsAndResponses] = useState([]);

  useEffect(() => {
    if (session.status === "unauthenticated") {
      setIsSignedIn(false);
    }
    if (session.status === "authenticated") {
      setIsSignedIn(true);
    }
  });

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        `https://vitalwebapp.onrender.com/dashboard`
      );
      const data = await response.json();
      setPromptsAndResponses(data);
    };
    fetchData();
  }, []);

  function formattedResponse(response) {
    let formattedResponse = response.replace(/\*/g, "•");

    formattedResponse = formattedResponse.replace(
      /\*\*(.*?)\*\*/g,
      "<b>$1</b>"
    );

    formattedResponse = formattedResponse.replace(/\n/g, "<br>");

    return <div dangerouslySetInnerHTML={{ __html: formattedResponse }} />;
  }

  return (
    <>
      {/* <AuthNavbar /> */}
      <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white">
        <h1 className="text-4xl mb-8 font-space">Dashboard</h1>
        {!isSignedIn && <VitalLoader />}
        <div className="grid grid-cols-1 gap-4 mx-10">
          {promptsAndResponses.map((item, index) => (
            <div key={index} className="p-4 rounded-lg shadow-md bg-gray-900">
              <h2 className="text-lg font-semibold mb-2">
                Prompt: {item.prompt}
              </h2>
              <p className="text-gray-400 px-4">
                Response: {formattedResponse(item.response)}
              </p>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default DashboardPage;
