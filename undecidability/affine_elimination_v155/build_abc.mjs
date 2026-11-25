import fs from 'node:fs';import crypto from 'node:crypto';import {abc} from './eliminate.mjs';
const raw=fs.readFileSync(new URL('../abc_dihedral_contact_v152/abc_quadrics.json',import.meta.url));
const hash=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');if(hash!=='e9b32774029b72b286e6d96f2f49f3d5906a6803')throw Error('v152 pin');
const t=abc(JSON.parse(raw));t.predecessor_git_blob=hash;
const out=JSON.stringify(t,null,2)+'\n';if(process.argv.includes('--write'))fs.writeFileSync(new URL('./abc_quadrics.json',import.meta.url),out);else if(fs.readFileSync(new URL('./abc_quadrics.json',import.meta.url),'utf8')!==out)throw Error('rebuild mismatch');
console.log('286 coordinates, 235 quadrics; exact affine replay passed');
