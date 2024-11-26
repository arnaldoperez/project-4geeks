import React, { useState, useEffect, useContext } from "react";
import { useSearchParams } from "react-router-dom";

import { Context } from "../store/appContext";

export const ChangePassword = () => {
  const { store, actions } = useContext(Context);
  let [params, setSearchParams] = useSearchParams();

  function submitForm(e) {
    e.preventDefault()
    const data = new FormData(e.target)
    let password = data.get("password")
    let verify = data.get("verifyPassword")
    if (password != verify) {
      alert("Las claves no coinciden")
      return
    }
    actions.changePassword(password, params.get("token"))
  }

  return (
    <div className="container">
      <form onSubmit={submitForm}>
        <div className="mb-3">
          <label for="password" className="form-label">Password</label>
          <input type="password" name="password" className="form-control" id="password" />
        </div>
        <div className="mb-3">
          <label for="verifyPassword" className="form-label">Password</label>
          <input type="password" name="verifyPassword" className="form-control" id="verifyPassword" />
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>
    </div>
  );
};
