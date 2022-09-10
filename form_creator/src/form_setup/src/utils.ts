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

/**Gets the CSRF token if it exists. */
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

/**
 * Returns null where the value is undefined, null or an empty string.
 * Otherwise returns the value.
 * @param value - The value to check.
 * @returns - The value if it is not null, undefined or an empty string.
 */
export const valueOrNull = (value: any) => {
  if (value === 0 || value === false) {
    return value;
  }
  return value || null;
};

/**Converts a value which represents a date time to a string representation of
 * itself.
 * @param dt - The date time value to convert.
 * @returns - The string representation of the date time.
 */
export const dateTimeToString = (dt: Date | string | undefined): string => {
  if (!dt) {
    return "";
  }
  if (typeof dt === "string") {
    return dt;
  }
  return dt.toISOString();
};

/**
 * Converts a string presentation of a date to another string presentation
 * which can be set as the value of an input element.
 * @param dtStr - The date time string to convert.
 * @returns - The converted date time string.
 */
export const dateTimeStrToInputVal = (dtStr: string): string => {
  const dt = new Date(dtStr);

  if (dt.toString() === "Invalid Date") {
    return "";
  }

  return dt.toISOString().slice(0, 16);
};
