/**
 * Response mapper
 */
export class ResponseMapper<T> {
  _propertyMapping: any;
  _typeList: any;
  _target: any;

  constructor(type: { new (): T }) {
    this._target = new type();
    this._propertyMapping = this._target.constructor._propertyMap;
    this._typeList = this._target.constructor._typeList;
  }

  findValueByKey(obj: any, key: any) {
    let result: any;
    for (let property in obj) {
      if (obj.hasOwnProperty(property)) {
        // If not null and match key return value
        if (property === key && obj[key] !== null) {
          return obj[key];
        }
      }
    }
    // Default return undefined
    return result;
  }

  map(source: any) {
    Object.keys(this._target).forEach((key) => {
      const mappedKey =
        this._propertyMapping !== undefined
          ? this._propertyMapping[key]
          : undefined;
      if (mappedKey) {
        this._target[key] = this.findValueByKey(source, mappedKey);
      } else {
        this._target[key] = this.findValueByKey(source, key);
      }
      if (typeof this._target[key] === 'object') {
        // If value is array callback each element
        if (Array.isArray(this._target[key])) {
          /**
           * Check condition is array.
           * if it is array to check element of array is object or not
           * if element is object, map element in array
           */
          if (typeof this._target[key][0] === 'object') {
            this._target[key] = this._target[key].map((item: any) =>
              new ResponseMapper(this._typeList[key]).map(item)
            );
          }
        } else {
          // If value is object only callback
          this._target[key] = new ResponseMapper(this._typeList[key]).map(
            this._target[key]
          );
        }
      }
    });
    return this._target;
  }
}
