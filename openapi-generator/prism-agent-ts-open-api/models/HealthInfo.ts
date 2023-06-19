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
 * @interface HealthInfo
 */
export interface HealthInfo {
    /**
     * The semantic version number of the running service
     * @type {string}
     * @memberof HealthInfo
     */
    version: string;
}

/**
 * Check if a given object implements the HealthInfo interface.
 */
export function instanceOfHealthInfo(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "version" in value;

    return isInstance;
}

export function HealthInfoFromJSON(json: any): HealthInfo {
    return HealthInfoFromJSONTyped(json, false);
}

export function HealthInfoFromJSONTyped(json: any, ignoreDiscriminator: boolean): HealthInfo {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'version': json['version'],
    };
}

export function HealthInfoToJSON(value?: HealthInfo | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'version': value.version,
    };
}
