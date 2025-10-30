import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Register from "./pages/Register/Register";
import Home from "./pages/Home/Home";     // nếu bạn có
import Login from "./pages/Login/Login";  // nếu bạn có

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />            {/* trang chủ */}
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        {/* Thêm route khác theo nhu cầu */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
