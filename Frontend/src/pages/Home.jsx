import React, { useState } from "react";

const Home = () => {
  const [dishName, setDishName] = useState('');
  const [dishData, setDishData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const getDishDetails = async (dishName) => {
    try {
      setLoading(true);
      setError('');
      const response = await fetch(`http://127.0.0.1:5000/api/get_dish_info/${encodeURIComponent(dishName)}`);
      if (!response.ok) {
        throw new Error('Dish not found');
      }
      const data = await response.json();
      setDishData(data);
    } catch (error) {
      console.error("Error fetching dish details:", error);
      setDishData(null);
      setError("Could not find dish details.");
    } finally {
      setLoading(false);
    }
  };

  const handleSearchClick = () => {
    if (dishName.trim()) {
      getDishDetails(dishName);
    } else {
      setError("Please enter a dish name.");
    }
  };

  const handleEnterButton = (e) => {
    if (e.key === 'Enter') {
      handleSearchClick();
    }
  };

  return (
    <div className="h-screen w-screen flex flex-col justify-center items-center px-4">
      <div className="w-full max-w-xl h-[50px] border-2 border-black rounded-2xl flex flex-row justify-between items-center mb-5">
        <input
          className="flex-1 h-full outline-none px-5 bg-transparent text-xl"
          placeholder="Enter a dish"
          type="text"
          value={dishName}
          onChange={(e) => setDishName(e.target.value)}
          onKeyDown={handleEnterButton}
        />
        <button
          className="bg-purple-800 w-[100px] h-full text-white rounded-2xl cursor-pointer"
          onClick={handleSearchClick}
        >
          Search
        </button>
      </div>

      {error && <div className="text-red-600 mb-3">{error}</div>}
      {loading && <div className="text-xl text-gray-500">Loading...</div>}

      {dishData && (
        <div className="w-full max-w-xl bg-gray-100 border border-gray-400 rounded-lg p-5 overflow-auto">
          <h2 className="text-xl font-bold">{dishData.dish_name}</h2>
          <p className="mt-2 text-lg">Dish Type: {dishData.dish_type}</p>

          <h3 className="mt-4 text-lg font-semibold">Ingredients:</h3>
          <ul className="list-disc pl-6">
            {dishData.ingredients_used.map((ingredient, index) => (
              <li key={index}>
                {ingredient.ingredient}: {ingredient.quantity}
              </li>
            ))}
          </ul>

          <h3 className="mt-4 text-lg font-semibold">
            Nutritional Information (per {dishData.category_weight}grams or {dishData.unit}):
          </h3>

          {(() => {
            const key = Object.keys(dishData).find(k => k.startsWith("estimated_nutrition_per_"));
            const nutritionInfo = key && dishData[key]?.nutrition ? dishData[key].nutrition : {};

            const fields = [
              { label: "Energy", key: "energy_kcal", unit: "kcal" },
              { label: "Carbohydrates", key: "carb_g", unit: "g" },
              { label: "Protein", key: "protein_g", unit: "g" },
              { label: "Fat", key: "fat_g", unit: "g" },
              { label: "Fibre", key: "fibre_g", unit: "g" },
              { label: "Calcium", key: "calcium_mg", unit: "mg" },
              { label: "Iron", key: "iron_mg", unit: "mg" },
              { label: "Sodium", key: "sodium_mg", unit: "mg" },
              { label: "Potassium", key: "potassium_mg", unit: "mg" }
            ];

            return (
              <ul className="list-none mt-2 space-y-1">
                {fields.map((item, index) => (
                  <li key={index}>
                    {item.label}: {nutritionInfo[item.key] ?? "N/A"} {item.unit}
                  </li>
                ))}
              </ul>
            );
          })()}
        </div>
      )}
    </div>
  );
};

export default Home;
