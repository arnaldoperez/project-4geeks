import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";

const Login = () => {

  const [loading, setLoading] = useState(false)
  const { actions } = useContext(Context)

  async function submitForm(e) {
    e.preventDefault()
    setLoading(true)
    let data = new FormData(e.target)
    let email = data.get("email")
    let password = data.get("password")
    if (!email || !password) {
      alert("Debe completar todos los campos")
      setLoading(false)
      return
    }
    await actions.login(email, password)
    setLoading(false)
  }
  return <>
    {loading ?
      <div className="d-flex align-items-center">
        <strong role="status">Loading...</strong>
        <div className="spinner-border ms-auto" style={{ "width": "3rem", "height": "3rem" }} aria-hidden="true"></div>
      </div> :
      <form onSubmit={submitForm}>
        <div className="mb-3">
          <label for="exampleInputEmail1" className="form-label">Email address</label>
          <input type="email" name="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" />
          <div id="emailHelp" className="form-text">We'll never share your email with anyone else.</div>
        </div>
        <div className="mb-3">
          <label for="exampleInputPassword1" className="form-label">Password</label>
          <input type="password" name="password" className="form-control" id="exampleInputPassword1" />
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>}
  </>

}
export default Login
