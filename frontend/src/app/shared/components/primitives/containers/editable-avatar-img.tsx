import React, {useState} from 'react';
import ImageUploader from 'react-images-upload';
import {KFlexColumn, KFlexRow} from 'src/app/shared/components/flex';
import KModal from 'src/app/shared/components/modal/k-modal';
import AvatarImg from 'src/app/shared/components/primitives/avatar-img';
import {KButton} from 'src/app/shared/components/primitives/buttons';
import styles from './editable-avatar-img.module.scss';

interface EditableAvatarImgProps {
    src: string;
    size: number;
    onSubmit: (file: File) => Promise<boolean>;
}

const EditableAvatarImg: React.FunctionComponent<EditableAvatarImgProps> = (
    {
        src,
        size,
        onSubmit
    }) => {
    const [modalOpen, setModalOpen] = useState(false);
    const [file, setFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);

    const avatarStyle: React.CSSProperties = {
        width: `${size}rem`,
        height: `${size}rem`,
    }

    const handleFileChange = (files: File[], pictures: string[]) => files.length > 0 && setFile(files[0])
    const handleCancel = () => setModalOpen(false);
    const handleSubmit = () => file && onSubmit(file).then(res => {
        if (!res) setError('server error try again later');
        setModalOpen(!res)
    })


    const imageUploader =
        <ImageUploader
            withIcon={true}
            singleImage={true}
            withPreview={true}
            buttonText='Choose images'
            onChange={handleFileChange}
            imgExtension={['.jpg', 'jpeg', '.png']}
            maxFileSize={5242880}
        />

    const modalBody =
        <>
            {imageUploader}
            {error &&
            <div className="c-danger">
                {error}
            </div>
            }
            <KFlexRow className="w-100" justify={'end'}>
                <KButton onClick={handleSubmit} color="primary" className="mr-2">Submit</KButton>
                <KButton onClick={handleCancel} color="danger">Cancel</KButton>
            </KFlexRow>
        </>

    const modal = <KModal body={modalBody} isOpen={modalOpen}/>

    return (
        <KFlexColumn className="position-relative" justify={'center'}>
            {modal}
            <AvatarImg src={src} size={size}/>
            <KButton type="button"
                     onClick={() => setModalOpen(true)}
                     style={avatarStyle}
                     className={`${styles.btnOverlay} round-image`}>
                    edit
            </KButton>
        </KFlexColumn>
    )
}

export default EditableAvatarImg;
