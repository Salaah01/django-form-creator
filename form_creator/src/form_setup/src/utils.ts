/**
 * Converts an array of objects into an object (dictionary like object).
 * @param {Array} array - Array to convert.
 * @param {String|Number} key - The key which will be become the key for each
 *  value. Must exist within each object within the array.
 */
export const arrayToObject = (array: object[], key: string | number) => {
  return array.reduce((obj: any, item: any) => {
    obj[item[key]] = item;
    return obj;
  }, {});
};



/**Gets the csrf_token if it exists. */
export const getCSRFToken = () => {
  for (const cookie of document.cookie.split("; ")) {
    if (cookie.startsWith("csrftoken")) {
      return cookie.split("=")[1];
    }
  }
  return;
};

/**Updates an oldObject using properties defined in a new object whilst
 * maintaining immutability by returning a copy of oldObject with the updated
 * properties.
 *
 * Args:
 *    oldObject: (obj) An object to be updated
 *    updatedProperties: (obj) An object consisting of properties to be
 *      added/updated onto the oldObject.
 */
export const updateObject = (
  oldObject: object,
  updatedProperties: object
): object => {
  return {
    ...oldObject,
    ...updatedProperties,
  };
};