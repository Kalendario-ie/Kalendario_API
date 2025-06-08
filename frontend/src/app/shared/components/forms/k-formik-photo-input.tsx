import {useFormikContext} from 'formik';
import React, {ChangeEvent, useEffect, useState} from 'react';
import {FormGroup, Input} from 'reactstrap';
import AvatarImg from 'src/app/shared/components/primitives/avatar-img';
import {KFlexRow} from 'src/app/shared/components/flex';

interface KFormikPhotoInputProps {
    name: string;
}

const KFormikPhotoInput: React.FunctionComponent<KFormikPhotoInputProps> = (
    {
        name
    }) => {
    const formik = useFormikContext();
    const fieldMeta = formik.getFieldMeta<string>(name);
    const helpers = formik.getFieldHelpers<string>(name);
    const [file, setFile] = useState('');

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files?.length > 0) {
            setFile(URL.createObjectURL(e.target.files[0]))
        }
    }

    useEffect(() => {
        setFile(fieldMeta.initialValue!);
    }, []);


    return (
        <FormGroup>
            <KFlexRow align={'center'} justify={'end'}>
                <AvatarImg size={5} src={file}/>
                <Input type="file" onChange={handleChange}/>
            </KFlexRow>
        </FormGroup>
    )
}


export default KFormikPhotoInput;
