import {loadStripe} from '@stripe/stripe-js';

const stripe_pk = process.env.REACT_APP_STRIPE_PK || '';

export const configureStripe = () => loadStripe(stripe_pk);
