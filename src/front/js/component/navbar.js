import React, { useContext, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext"
import { useNavigate } from "react-router-dom";

export const Navbar = () => {
  const { store, actions } = useContext(Context)
  const navigate = useNavigate()
  const modal = useRef(null);


  useEffect(() => {
    if (!modal) return
    console.log({ fetching: store.fetching })
    const modal = new bootstrap.Modal(modal.current)
    if (store.fetching) {
      modal.show
    } else {
      modal.hide
    }
  }, [store.fetching])

  function buttonClick() {
    if (store.token) {
      actions.logout()
      return
    }
    navigate("/")
  }
  return (
    <nav className="navbar navbar-light bg-light">
      <div ref={modal} className="modal fade" id="modal-loading" aria-hidden="true" aria-labelledby="exampleModalToggleLabel">
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content">
            <div className="spinner-border text-primary" style={{ "width": "3rem", "height": "3rem" }} role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        </div>
      </div>
      <div className="container">
        <Link to="/">
          <span className="navbar-brand mb-0 h1">React Boilerplate</span>
        </Link>
        <div className="ml-auto">
          <button onClick={buttonClick} className="btn btn-primary">{
            store.token ? "Logout" : "Home"
          }</button>
        </div>
      </div>

    </nav>
  );
};
