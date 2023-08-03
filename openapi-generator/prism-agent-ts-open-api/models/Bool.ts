/* tslint:disable */
/* eslint-disable */
/**
 * Prism Agent
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface Bool
 */
export interface Bool {
    /**
     * 
     * @type {boolean}
     * @memberof Bool
     */
    value: boolean;
}

/**
 * Check if a given object implements the Bool interface.
 */
export function instanceOfBool(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "value" in value;

    return isInstance;
}

export function BoolFromJSON(json: any): Bool {
    return BoolFromJSONTyped(json, false);
}

export function BoolFromJSONTyped(json: any, ignoreDiscriminator: boolean): Bool {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'value': json['value'],
    };
}

export function BoolToJSON(value?: Bool | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'value': value.value,
    };
}

