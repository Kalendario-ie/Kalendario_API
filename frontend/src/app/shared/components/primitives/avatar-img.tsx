import React from 'react';

interface AvatarImgProps {
    src: string;
    size?: number;
    className?: string;
    alt?: string;
    id?: string;
}

const AvatarImg: React.FunctionComponent<AvatarImgProps> = (
    {
        src,
        size= 7,
        alt,
        className = '',
        id
    }) => {
    const avatarStyle = {
        width: `${size}rem`,
        height: `${size}rem`
    }
    className += " round-image";
    return (
        <img className={className} src={src} alt={alt} style={avatarStyle} id={id}/>
    )
}

export default AvatarImg;
