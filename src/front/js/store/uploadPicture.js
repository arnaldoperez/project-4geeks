import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";

const UploadPicture = () => {

  const [loading, setLoading] = useState(false)
  const { actions } = useContext(Context)

  async function submitForm(e) {
    e.preventDefault()
    setLoading(true)
    let data = new FormData(e.target)
    if (!data.get("profilePicture")) {
      alert("Debe completar todos los campos")
      setLoading(false)
      return
    }
    let resp = await actions.uploadPicture(data)
    if (resp) {
      alert("Imagen actualizada")
    } else {
      alert("Error al cargar la imagen")
    }
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
          <label htmlFor="formFile" className="form-label">Default file input example</label>
          <input className="form-control" name="profilePicture" type="file" id="formFile" />
          <input className="form-control" name="name" type="text" id="formFile" />
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>}
  </>

}
export default UploadPicture
