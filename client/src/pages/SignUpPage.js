import React from "react";
import { useNavigate, Link } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import api from "../api/axiosInstance"; // make sure axiosInstance is set

function SignUpPage() {
  const navigate = useNavigate();

  const initialValues = {
    username: "",
    password: "",
  };

  const validationSchema = Yup.object({
    username: Yup.string()
      .min(3, "Username must be at least 3 characters")
      .required("Username is required"),
    password: Yup.string()
      .matches(
        /^(?=.*[A-Z])(?=.*[^A-Za-z0-9]).{8,}$/,
        "Password must be 8+ chars, 1 capital, 1 symbol"
      )
      .required("Password is required"),
  });

  const checkUsername = async (username) => {
    if (!username) return false;
    try {
      const res = await api.get(`/api/users/check-username`, {
        params: { username },
      });
      return res.data.available;
    } catch {
      return false;
    }
  };

  const handleSubmit = async (values, { setSubmitting, setFieldError, setStatus }) => {
    const usernameAvailable = await checkUsername(values.username);
    if (!usernameAvailable) {
      setFieldError("username", "Username not available");
      setSubmitting(false);
      return;
    }

    try {
      // ✅ Register user
      const res = await api.post("/api/users/register", values);

      if (res.status === 201) {
        // ✅ Immediately log in
        const loginRes = await api.post("/api/users/login", values);
        const token = loginRes.data.access_token;

        // ✅ Store JWT token
        localStorage.setItem("token", token);

        setStatus("Registration successful! Redirecting...");
        setTimeout(() => navigate("/"), 1500);
      } else {
        setStatus("Registration failed.");
      }
    } catch (err) {
      const msg = err.response?.data?.error || "Something went wrong. Try again.";
      setStatus(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-form-wrapper">
      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, status, setFieldError, setFieldTouched }) => (
          <Form className="auth-form">
            <h1>Sign Up</h1>

            <div>
              <label>Username: </label>
              <Field
                name="username"
                onBlur={async (e) => {
                  setFieldTouched("username", true);
                  const available = await checkUsername(e.target.value);
                  if (!available) {
                    setFieldError("username", "Username not available");
                  }
                }}
              />
              <ErrorMessage name="username" component="div" style={{ color: "red" }} />
            </div>

            <div>
              <label>Password: </label>
              <Field type="password" name="password" />
              <ErrorMessage name="password" component="div" style={{ color: "red" }} />
            </div>

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Registering..." : "Register"}
            </button>

            {status && <div style={{ marginTop: "1em", color: "blue" }}>{status}</div>}

            <div style={{ marginTop: "1em" }}>
              Already have an account?{" "}
              <Link to="/login">
                <button type="button">Login instead</button>
              </Link>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default SignUpPage;
