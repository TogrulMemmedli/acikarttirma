
import { Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import HomePage from "./App";
import Register from "./pages/Register";
import Login from "./pages/Login";
import VerifyEmail from "./pages/VerifyEmail";

export default function AppRouter() {
  return (
    <>
      <Header />

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/verify-email" element={<VerifyEmail />} />
      </Routes>
    </>
  );
}
