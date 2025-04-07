/**
 * Base mapper class to provide mapping functionality
 */
export class BaseMapper {
  /**
   * Map from source to target type
   * @param source Source object
   * @param targetType Target class type
   */
  static map<T>(source: any, targetType: new () => T): T {
    if (!source) {
      return null as unknown as T; // Explicitly cast null to T to satisfy the type checker
    }

    const target = new targetType() as Record<string, any>; // Use Record<string, any> for dynamic property assignment
    const propertyMap: Record<string, string> = targetType.prototype.constructor._propertyMap || {};
    const typeList: Record<string, new () => any> = targetType.prototype.constructor._typeList || {};

    Object.keys(propertyMap).forEach(key => {
      const sourceKey = propertyMap[key];
      const type = typeList[key];

      // Get value from source using the mapped source property name
      const value = this.getValueFromPath(source, sourceKey);

      if (value !== undefined) {
        // If type is provided and value is not null, map it recursively
        if (type && value !== null) {
          if (Array.isArray(value)) {
            // Handle array of objects
            target[key] = value.map(item => this.map(item, type));
          } else {
            // Handle single object
            target[key] = this.map(value, type);
          }
        } else {
          // Handle primitive types
          target[key] = value;
        }
      }
    });

    return target as T; // Cast target back to T
  }

  /**
   * Map an array of objects
   * @param sourceArray Array of source objects
   * @param targetType Target class type
   */
  static mapArray<T>(sourceArray: any[], targetType: new () => T): T[] {
    if (!sourceArray) {
      return [];
    }
    return sourceArray.map(item => this.map(item, targetType));
  }

  /**
   * Get value from nested object path like "user.address.street"
   */
  private static getValueFromPath(obj: any, path: string): any {
    if (!obj || !path) {
      return undefined;
    }
    
    const parts = path.split('.');
    let current = obj;
    
    for (let i = 0; i < parts.length; i++) {
      if (current === null || current === undefined) {
        return undefined;
      }
      current = current[parts[i]];
    }
    
    return current;
  }
}