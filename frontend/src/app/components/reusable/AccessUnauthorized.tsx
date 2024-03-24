const AccessUnauthorized = () => {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8 text-center">Found Items</h1>
        <div className="flex flex-col text-center justify-center bg-red-300 text-black font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-300 w-fit mx-auto">
          <p>You are not authorized to view this page.</p>
          <p>Please login to continue.</p>
        </div>
      </div>
    );
  };
  
  export default AccessUnauthorized;