/**
 * Mapping the property
 * @param sourceProperty -> source property
 * @param type -> type of class (use for Object class, no need you for primitive types)
 */
export function propertyMapper(sourceProperty: string, type?: any) {
  return function (target: any, propertyKey: string) {
    if (!target.constructor._propertyMap) {
      target.constructor._propertyMap = {};
    }
    target.constructor._propertyMap[propertyKey] = sourceProperty;
    if (!target.constructor._typeList) {
      target.constructor._typeList = {};
    }
    target.constructor._typeList[propertyKey] = type;
  };
}
