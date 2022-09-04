const DJANGO_DEV_HOST = process.env.REACT_APP_DJANGO_DEV_HOST || "localhost";
const DJANGO_DEV_PORT = process.env.REACT_APP_DJANGO_DEV_PORT || "8000";

/**Depending on what the environment is, either use "/" as the root URL or
 * explicity set the host and port for the Django server.
 */
export const rootURL =
  process.env.NODE_ENV === "production"
    ? "/"
    : `http://${DJANGO_DEV_HOST}:${DJANGO_DEV_PORT}/`;

/**
 * Retrieve an API endpoint.
 * @param urlName - The name of the endpoint to retrieve.
 * @param inputElemID - The ID of the input element that contains the url name
 *  to view.
 * @param pk - The primary key of the object to retrieve.
 * @returns - The URL of the endpoint.
 */
const getAPIEndpoint = (
  urlName: string,
  inputElemID: string,
  pk: number | null = null
): string => {
  const inputElem = document.getElementById(
    inputElemID
  ) as HTMLInputElement | null;
  if (inputElem) {
    return inputElem.value;
  }

  const apiRoot = `${rootURL}form-creator/api/`;

  switch (urlName) {
    case "api-root":
      return apiRoot;

    case "form-list":
      return `${apiRoot}forms/`;

    case "form-detail":
      if (!pk) {
        throw new Error("No pk provided for form-detail");
      }
      return `${apiRoot}forms/${pk}/`;

    case "form-element-list":
      return `${apiRoot}form-elements/`;

    case "form-element-detail":
      if (!pk) {
        throw new Error("No pk provided for form-element-detail");
      }
      return `${apiRoot}form-elements/${pk}/`;

    case "form-element-html-component":
      if (!pk) {
        throw new Error("No pk provided for html-component");
      }
      return `${apiRoot}html-components/${pk}/`;

    case "form-element-form-question":
      if (!pk) {
        throw new Error("No pk provided for form-question");
      }
      return `${apiRoot}form-questions/${pk}/`;

    default:
      throw new Error(`Unknown urlName: ${urlName}`);
  }
};

export default getAPIEndpoint;
