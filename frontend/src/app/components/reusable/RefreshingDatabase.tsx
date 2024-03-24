const RefreshingDatabase = () => {
    return (
      <div className="flex justify-center items-start h-screen">
        <div className="bg-white border py-8 px-12 rounded-lg shadow-lg">
          <p className="text-lg text-gray-800">Refreshing Database...</p>
          <div className="mt-4 flex justify-center">
            <div className="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-12 w-12"></div>
          </div>
        </div>
      </div>
    );
  };
  
  export default RefreshingDatabase;