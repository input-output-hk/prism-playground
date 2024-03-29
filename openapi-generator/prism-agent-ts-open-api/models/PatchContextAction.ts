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
 * @interface PatchContextAction
 */
export interface PatchContextAction {
    /**
     * 
     * @type {Array<string>}
     * @memberof PatchContextAction
     */
    contexts?: Array<string>;
}

/**
 * Check if a given object implements the PatchContextAction interface.
 */
export function instanceOfPatchContextAction(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function PatchContextActionFromJSON(json: any): PatchContextAction {
    return PatchContextActionFromJSONTyped(json, false);
}

export function PatchContextActionFromJSONTyped(json: any, ignoreDiscriminator: boolean): PatchContextAction {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'contexts': !exists(json, 'contexts') ? undefined : json['contexts'],
    };
}

export function PatchContextActionToJSON(value?: PatchContextAction | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'contexts': value.contexts,
    };
}

