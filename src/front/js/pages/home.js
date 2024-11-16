import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import Login from "../component/login";
import UploadPicture from "../store/uploadPicture";

export const Home = () => {
  const { store, actions } = useContext(Context);

  return (
    <div className="text-center mt-5">
      {store.token ?
        <>
          <UploadPicture />
          {store.profilePicture ? <img src={store.profilePicture} class="img-fluid" alt="..." /> : ""}
        </>
        :
        <Login />
      }

      <p>
        This boilerplate comes with lots of documentation:{" "}
        <a href="https://start.4geeksacademy.com/starters/react-flask">
          Read documentation
        </a>
      </p>
    </div>
  );
};
