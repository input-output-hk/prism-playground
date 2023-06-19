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
 * @interface RequestPresentationOutput
 */
export interface RequestPresentationOutput {
    /**
     * Ref to the id on the presentation (db ref)
     * @type {string}
     * @memberof RequestPresentationOutput
     */
    presentationId: string;
}

/**
 * Check if a given object implements the RequestPresentationOutput interface.
 */
export function instanceOfRequestPresentationOutput(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "presentationId" in value;

    return isInstance;
}

export function RequestPresentationOutputFromJSON(json: any): RequestPresentationOutput {
    return RequestPresentationOutputFromJSONTyped(json, false);
}

export function RequestPresentationOutputFromJSONTyped(json: any, ignoreDiscriminator: boolean): RequestPresentationOutput {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'presentationId': json['presentationId'],
    };
}

export function RequestPresentationOutputToJSON(value?: RequestPresentationOutput | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'presentationId': value.presentationId,
    };
}
