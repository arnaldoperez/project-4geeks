import React, { useState, useEffect, useContext } from "react";
import { useSearchParams } from "react-router-dom";

import { Context } from "../store/appContext";

export const ChangePassword = () => {
	const { store, actions } = useContext(Context);
  let [params, setSearchParams] = useSearchParams();

  function submitForm(e){
    e.preventDefault()
    const data=new FormData(e.target)
    let password=data.get("password")
    let verify=data.get("verifyPassword")
    if(password!=verify){
      alert("Las claves no coinciden")
      return
    }
    actions.changePassword(password,params.get("token"))
  }

	return (
		<div className="container">
			<form onSubmit={submitForm}>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" name="password" class="form-control" id="password" />
        </div>
        <div class="mb-3">
          <label for="verifyPassword" class="form-label">Password</label>
          <input type="password" name="verifyPassword" class="form-control" id="verifyPassword" />
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
		</div>
	);
};
