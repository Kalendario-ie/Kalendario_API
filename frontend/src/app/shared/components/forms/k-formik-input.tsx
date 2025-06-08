import {ErrorMessage, Field, FieldInputProps, useFormikContext} from 'formik';
import * as React from 'react';
import {FormFeedback, FormGroup, Label} from 'reactstrap';
import {KFormikInputBaseProps} from 'src/app/shared/components/forms/interfaces';
import {KCheckbox, KColorInput, KDurationInput, KMultiSelectInput} from 'src/app/shared/components/primitives/inputs';
import {MultiSelectOption} from 'src/app/shared/components/primitives/inputs/interfaces';
import {camelCaseToWords} from 'src/app/shared/util/string-extensions';

export interface KFormikInputProps extends KFormikInputBaseProps {
    options?: MultiSelectOption[];
    multiple?: boolean;
    emptyOption?: boolean;
    as?: string;
    className?: string;
}

function inputAs(as: string,
                 options: { id: number; name: string }[] | undefined
): string | React.FunctionComponent<any> {
    switch (as) {
        case 'duration':
            return KDurationInput
        case 'color':
            return KColorInput
        case 'multi-select':
            return (fieldProps: FieldInputProps<any>) =>
                <KMultiSelectInput
                    name={fieldProps.name}
                    value={fieldProps.value}
                    onChange={fieldProps.onChange}
                    onBlur={fieldProps.onBlur}
                    options={options || []}
                />
        case 'checkbox':
            return KCheckbox
        default:
            return as;
    }
}

export const KFormikInput: React.FunctionComponent<KFormikInputProps> = (
    {
        name,
        placeholder,
        type,
        options,
        multiple = false,
        emptyOption = true,
        as = 'input',
        className = '',
    }
) => {
    const formik = useFormikContext();
    const fieldMeta = formik.getFieldMeta(name);
    const fieldHelpers = formik.getFieldHelpers(name);
    const fieldClassName = `form-control ${(fieldMeta.error && fieldMeta.touched) ? ' is-invalid' : ''} ${multiple ? ' form-select form-control' : ''}`
    const isCheckbox = as === 'checkbox';
    const inputType = React.useMemo(() => inputAs(as, options), [options, as]);

    const handleOnEmptySelect = () => fieldHelpers.setValue(null);

    return (
        <FormGroup className={className} check={isCheckbox}>
            {!isCheckbox &&
            <Label for={name} className="ml-1 mb-1">{placeholder || camelCaseToWords(name)}</Label>
            }
            <Field className={fieldClassName}
                   as={inputType}
                   id={name}
                   name={name}
                   type={type}
                   multiple={multiple}
                   placeholder={placeholder || name}>
                {options &&
                <>
                    {emptyOption && !multiple && <option onClick={handleOnEmptySelect} value=""/>}
                    {options.map((option) =>
                        <option key={option.id} value={option.id}>{option.name}</option>)
                    }
                </>
                }
            </Field>
            <FormFeedback>
                <ErrorMessage name={name}/>
            </FormFeedback>
        </FormGroup>
    )
}

