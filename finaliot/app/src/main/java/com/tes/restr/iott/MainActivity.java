package com.tes.restr.iott;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.ToggleButton;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {
    // Write a message to the database
    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference refHome = database.getReference("home");
    DatabaseReference refled, refButton, refDled, refDbutton,refDeep;
    ToggleButton btnToggle; // 버튼 눌렀을때 led on 되거나 off되는 부분
    TextView b_state_t;// 이부분 버튼 눌렀을때 text true or false 되는 부분
    Switch aSwitch,Dswitch;
    ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.m_main);
        refled = refHome.child("led");
        refDled = refled.child("d_led");

        refButton = refHome.child("button");
        refDbutton = refButton.child("d_button");

        refDeep=refHome.child("deep_state");
/*
        btnToggle = (ToggleButton)  findViewById(R.id.toggleButton);
        btnToggle.setTextOn("N_state_ON");
        btnToggle.setTextOff("N_state_OFF");
*/
        imageView = (ImageView) findViewById(R.id.led1);
        aSwitch = (Switch) findViewById(R.id.switch1);
        Dswitch = (Switch) findViewById(R.id.deep_switch);
        final Button deepv = (Button) findViewById(R.id.deep_view);

        b_state_t = (TextView) findViewById(R.id.b_state);

        //controlLED(refDled, btnToggle);
        controlLED(refDled, aSwitch);

        //gdb_state(refDbutton, b_state_t);//버튼 관련 firebase에서 가져오는 자료.

        deepv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this,deep.class);
                startActivity(intent);
                finish();

            }
        });

        Dswitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    //refDeep.setValue(isChecked);// The toggle is enabled
                    refDeep.setValue(isChecked);
                } else {
                    // The toggle is disabled
                    refDeep.setValue(isChecked);// The toggle is enabled
                }
            }
        });
        refDeep.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                Boolean dled  = (Boolean) dataSnapshot.getValue();
                Dswitch.setChecked(dled);
                if(dled){
                    //awSwitch.setTextOn("Led_on");

                } else {
                    //awSwitch.setTextOff("Led_off");
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) { }

        });

    }
    //private void controlLED(final DatabaseReference refLed, final ToggleButton toggle_btn ) {
    private void controlLED(final DatabaseReference refLed, final Switch awSwitch ) {
/*
        toggle_btn.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean isChecked) {
                refLed.setValue(isChecked);
            }
        });
*/
        awSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    refLed.setValue(isChecked);// The toggle is enabled
                    imageView.setImageResource(R.drawable.lon);
                } else {
                    // The toggle is disabled
                    refLed.setValue(isChecked);// The toggle is enabled
                    imageView.setImageResource(R.drawable.loff);
                }
            }
        });



        refLed.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                Boolean dled  = (Boolean) dataSnapshot.getValue();
                awSwitch.setChecked(dled);
                if(dled){
                    //awSwitch.setTextOn("Led_on");

                } else {
                    //awSwitch.setTextOff("Led_off");
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) { }

        });
    }

}
